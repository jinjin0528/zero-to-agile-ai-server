"""매물과 가까운 대학(본교) 5곳 거리 확인 러너."""
from __future__ import annotations

import argparse
import math
import os
import sys

from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from infrastructure.db.postgres import SessionLocal, get_db_session
from infrastructure.db.session_helper import open_session
from modules.house_platform.infrastructure.orm.house_platform_orm import (
    HousePlatformORM,
)
from modules.house_platform.infrastructure.repository.house_platform_repository import (
    HousePlatformRepository,
)
from modules.university.adapter.output.university_repository import (
    UniversityRepository,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--house-platform-id", type=int, default=None)
    parser.add_argument("--limit", type=int, default=5)
    return parser.parse_args()


def _find_sample_house_platform_id() -> int | None:
    session, generator = open_session(get_db_session)
    try:
        row = (
            session.query(HousePlatformORM.house_platform_id)
            .filter(HousePlatformORM.lat_lng.isnot(None))
            .filter(
                (HousePlatformORM.is_banned.is_(False))
                | (HousePlatformORM.is_banned.is_(None))
            )
            .order_by(HousePlatformORM.house_platform_id.asc())
            .first()
        )
        return int(row[0]) if row else None
    finally:
        if generator:
            generator.close()
        else:
            session.close()


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """위경도 직선 거리를 계산한다."""
    radius_km = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def _estimate_walk_minutes(distance_km: float) -> float:
    """도보 이동 시간을 추정한다."""
    # 도보 평균 속도 4.8km/h 기준 (분당 80m)
    return (distance_km / 4.8) * 60


def _normalize_university_name(name: str) -> str:
    """대학명에서 본교 기준 대표 이름을 추출한다."""
    if not name:
        return ""
    token = "대학교"
    idx = name.find(token)
    if idx == -1:
        return name.strip()
    return name[: idx + len(token)].strip()


def main() -> None:
    load_dotenv()
    args = parse_args()

    house_platform_id = (
        args.house_platform_id or _find_sample_house_platform_id()
    )
    if not house_platform_id:
        print("house_platform 위치 정보가 있는 데이터가 없습니다.")
        return

    house_repo = HousePlatformRepository()
    house_location = house_repo.fetch_location_by_id(house_platform_id)
    if not house_location:
        print("선택한 매물의 위치 정보가 없습니다.")
        return

    university_repo = UniversityRepository(SessionLocal)
    universities = university_repo.get_university_locations()
    if not universities:
        print("대학 위치 정보가 없습니다.")
        return

    distances = []
    for university in universities:
        if university.campus != "본교":
            continue
        base_name = _normalize_university_name(university.university_name)
        km = _haversine_km(
            house_location.lat,
            house_location.lng,
            university.lat,
            university.lng,
        )
        minutes = _estimate_walk_minutes(km)
        distances.append(
            {
                "university_name": base_name,
                "campus": university.campus,
                "distance_km": km,
                "minutes_to_school": minutes,
            }
        )

    # 같은 대학교(본교)는 하나만 남긴다.
    unique_by_name = {}
    for item in distances:
        key = item["university_name"]
        existing = unique_by_name.get(key)
        if not existing or item["distance_km"] < existing["distance_km"]:
            unique_by_name[key] = item

    sorted_distances = sorted(
        unique_by_name.values(), key=lambda item: item["distance_km"]
    )
    top = sorted_distances[: max(1, args.limit)]

    print(
        f"house_platform_id={house_platform_id} 위치 기반 가까운 대학 {len(top)}곳"
    )
    for idx, item in enumerate(top, start=1):
        print(
            f"{idx}. {item['university_name']} {item['campus']} "
            f"{item['distance_km']:.3f}km "
            f"({item['minutes_to_school']:.1f}분)"
        )

    # TODO: 실제 서비스에서는 도보/대중교통 API를 사용해 이동 시간을 보정한다.


if __name__ == "__main__":
    main()
