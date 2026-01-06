from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DistanceObservationFeatures:
    학교까지_분: float
    거리_백분위: float
    거리_버킷: str
    거리_비선형_점수: float

    def __post_init__(self):
        if self.학교까지_분 < 0:
            raise ValueError(f"학교까지 최소 거리는 0 이상이어야 합니다. 입력값: {self.학교까지_분}")

        if not (0.0 <= self.거리_백분위 <= 1.0):
            raise ValueError(f"거리 백분위는 0 이상 1 이하이어야 합니다. 입력값: {self.거리_백분위}")

        if not self.거리_버킷:
            raise ValueError("거리 구간(bucket)은 비어 있을 수 없습니다.")

        if self.거리_비선형_점수 < 0:
            raise ValueError(f"거리 비선형 점수는 0 이상이어야 합니다. 입력값: {self.거리_비선형_점수}")

    @classmethod
    def from_raw(cls, raw: Dict) -> "DistanceObservationFeatures":
        if raw is None:
            raise ValueError("Distance raw data is required to create DistanceObservationFeatures")

        return cls(
            학교까지_분=raw["minutes_to_school"],
            거리_백분위=raw["distance_percentile"],
            거리_버킷=raw["distance_bucket"],
            거리_비선형_점수=raw["nonlinear_distance_score"],
        )
