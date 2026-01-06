from datetime import datetime, timezone

from modules.house_platform.application.port_out.house_platform_repository_port import HousePlatformRepositoryPort
from modules.observations.application.assembler.observation_raw_assembler import ObservationRawAssembler
from modules.observations.application.port.observation_repository_port import ObservationRepositoryPort
from modules.observations.domain.model.student_recommendation_feature_observation import StudentRecommendationFeatureObservation
from modules.observations.domain.value_objects.convenience_observation_features import ConvenienceObservationFeatures
from modules.observations.domain.value_objects.distance_observation_features import DistanceObservationFeatures
from modules.observations.domain.value_objects.observation_metadata import ObservationMetadata
from modules.observations.domain.value_objects.observation_notes import ObservationNotes
from modules.observations.domain.value_objects.price_observation_features import PriceObservationFeatures
from modules.observations.domain.value_objects.risk_observation_features import RiskObservationFeatures


class HouseNotFoundError(Exception):
    def __init__(self, house_id: int):
        super().__init__(f"House with ID {house_id} not found.")


class GenerateObservationUseCase:

    def __init__(
        self,
        observation_repo: ObservationRepositoryPort,
        raw_house_repo: HousePlatformRepositoryPort,
    ):
        self.observation_repo = observation_repo
        self.raw_house_repo = raw_house_repo

    def execute(self, house_id: int) -> StudentRecommendationFeatureObservation:
        bundle = self.raw_house_repo.fetch_bundle_by_id(house_id)
        if not bundle or not bundle.house_platform:
            raise HouseNotFoundError(house_id)

        raw_house = bundle.house_platform
        options = bundle.options  # 없을 수 있음

        # ---- price ----
        price_raw = ObservationRawAssembler.build_price_raw(raw_house)
        price_features = PriceObservationFeatures.from_raw(price_raw)

        # ---- convenience ----
        convenience_features = None
        if options:
            convenience_raw = ObservationRawAssembler.build_convenience_raw(options)
            convenience_features = ConvenienceObservationFeatures.from_raw(convenience_raw)

        # ---- distance ----
        distance_raw = None
        if raw_house:
            distance_raw = {
                "minutes_to_school": 9999.0,
                "distance_bucket": "UNKNOWN",
                "distance_percentile": 0.0,
                "nonlinear_distance_score": 0.0,
            }

        distance_features = DistanceObservationFeatures.from_raw(distance_raw)

        # ---- risk ----
        risk_raw = ObservationRawAssembler.build_risk_raw(raw_house)
        risk_features = RiskObservationFeatures.from_raw(risk_raw)

        metadata = ObservationMetadata.from_raw(raw_house)

        observation = StudentRecommendationFeatureObservation(
            platform_id=house_id,
            snapshot_id=raw_house.snapshot_id,
            가격_관측치=price_features,
            거리_관측치=distance_features,
            위험_관측치=risk_features,
            편의_관측치=convenience_features,
            관측_메모=ObservationNotes.empty(),
            메타데이터=metadata,
            calculated_at=datetime.now(timezone.utc),
        )

        self.observation_repo.save(observation)
        return observation
