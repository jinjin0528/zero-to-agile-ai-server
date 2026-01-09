from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HousePlatformLocation:
    """매물 경위도 정보."""

    house_platform_id: int
    lat: float
    lng: float
