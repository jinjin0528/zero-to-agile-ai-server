"""student_house_decision_policy finder_request 기반 필터링 러너."""
from __future__ import annotations

import argparse
import os
import sys

from dotenv import load_dotenv

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from infrastructure.db.postgres import SessionLocal, get_db_session
from modules.finder_request.adapter.output.repository.finder_request_repository import (
    FinderRequestRepository,
)
from modules.student_house_decision_policy.application.dto.candidate_filter_dto import (
    FilterCandidateCommand,
)
from modules.student_house_decision_policy.application.dto.candidate_filter_dto import (
    ObservationPriceFeatures,
)
from modules.student_house_decision_policy.application.usecase.filter_candidate import (
    FilterCandidateService,
)
from modules.student_house_decision_policy.domain.value_object.budget_filter_policy import (
    BudgetFilterPolicy,
)
from modules.student_house_decision_policy.infrastructure.repository.house_platform_candidate_repository import (
    HousePlatformCandidateRepository,
)
from modules.house_platform.infrastructure.orm.house_platform_orm import (
    HousePlatformORM,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finder-request-id", type=int, required=True)
    parser.add_argument(
        "--budget-margin-ratio",
        type=float,
        default=None,
        help="예산 여유율(기본값은 Policy 기본값 사용)",
    )
    parser.add_argument(
        "--display-limit",
        type=int,
        default=10,
        help="출력용 후보 표시 개수",
    )
    return parser.parse_args()


class MockObservationPriceRepository:
    """house_platform 원본을 관측치로 변환하는 mock 저장소."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    def fetch_price_features(
        self, house_platform_id: int, snapshot_id: str
    ) -> ObservationPriceFeatures | None:
        session = self._session_factory()
        try:
            row = (
                session.query(
                    HousePlatformORM.house_platform_id,
                    HousePlatformORM.snapshot_id,
                    HousePlatformORM.deposit,
                    HousePlatformORM.monthly_rent,
                    HousePlatformORM.manage_cost,
                )
                .filter(HousePlatformORM.house_platform_id == house_platform_id)
                .one_or_none()
            )
            if not row:
                return None
            if row[1] != snapshot_id:
                return None
            deposit = int(row[2] or 0)
            monthly_rent = int(row[3] or 0)
            manage_cost = int(row[4] or 0)
            estimated_move_in_cost = deposit + monthly_rent + manage_cost
            monthly_cost_est = monthly_rent + manage_cost
            return ObservationPriceFeatures(
                house_platform_id=house_platform_id,
                snapshot_id=snapshot_id,
                estimated_move_in_cost=estimated_move_in_cost,
                monthly_cost_est=monthly_cost_est,
                price_percentile=0.5,
                price_zscore=0.0,
                price_burden_nonlinear=min(monthly_cost_est / 100.0, 1.0),
            )
        finally:
            session.close()


def main() -> None:
    load_dotenv()
    args = parse_args()

    db_gen = get_db_session()
    db = next(db_gen)
    try:
        finder_request_repo = FinderRequestRepository(db)
        house_platform_repo = HousePlatformCandidateRepository()
        observation_repo = MockObservationPriceRepository(SessionLocal)
        policy = (
            BudgetFilterPolicy(budget_margin_ratio=args.budget_margin_ratio)
            if args.budget_margin_ratio is not None
            else BudgetFilterPolicy()
        )
        usecase = FilterCandidateService(
            finder_request_repo,
            house_platform_repo,
            observation_repo,
            policy=policy,
        )

        result = usecase.execute(
            FilterCandidateCommand(finder_request_id=args.finder_request_id)
        )

        print(f"finder_request_id={result.finder_request_id}")
        print(
            "criteria: "
            f"deposit_limit={result.criteria.max_deposit_limit} "
            f"rent_limit={result.criteria.max_rent_limit} "
            f"margin_ratio={result.criteria.budget_margin_ratio}"
        )
        print(
            "filters: "
            f"price_type={result.criteria.price_type} "
            f"preferred_region={result.criteria.preferred_region} "
            f"house_type={result.criteria.house_type}"
        )
        if result.message:
            print(f"message={result.message}")
            return

        candidates = list(result.candidates)
        print(f"candidates: {len(candidates)}")
        for idx, item in enumerate(candidates[: args.display_limit], start=1):
            print(
                f"{idx}. house_platform_id={item.house_platform_id} "
                f"deposit={item.deposit} "
                f"monthly_rent={item.monthly_rent} "
                f"manage_cost={item.manage_cost} "
                f"snapshot_id={item.snapshot_id}"
            )
    finally:
        db_gen.close()


if __name__ == "__main__":
    main()
