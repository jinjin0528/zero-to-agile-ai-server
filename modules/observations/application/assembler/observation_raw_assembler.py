from modules.house_platform.application.dto.house_platform_dto import HousePlatformUpsertModel, \
    HousePlatformOptionUpsertModel


class ObservationRawAssembler:
    @staticmethod
    def build_price_raw(
            house: HousePlatformUpsertModel,
    ) -> dict:
        total_monthly_cost = (
                (house.monthly_rent or 0)
                + (house.manage_cost or 0)
        )

        return {
            "price_percentile": None,  # 외부 통계 주입
            "price_zscore": None,  # 외부 통계 주입
            "expected_move_in_cost": house.deposit or 0,
            "monthly_cost_estimate": total_monthly_cost,
            "nonlinear_price_burden": None,  # 후처리
        }

    @staticmethod
    def build_convenience_raw(
            options: HousePlatformOptionUpsertModel,
    ) -> dict:
        coverage = sum([
            bool(options.built_in),
            options.near_univ,
            options.near_transport,
            options.near_mart,
        ]) / 4.0

        return {
            "essential_option_coverage": coverage,
            "convenience_score": coverage,
        }

    @staticmethod
    def build_distance_raw(
            minutes_to_school: float,
            distance_bucket: str,
            distance_percentile: float,
    ) -> dict:
        return {
            "minutes_to_school": minutes_to_school,
            "distance_bucket": distance_bucket,
            "distance_percentile": distance_percentile,
            "nonlinear_distance_score": 1 / (1 + minutes_to_school),
        }

    @staticmethod
    def build_risk_raw(
            house: HousePlatformUpsertModel,
    ) -> dict:
        return {
            "is_banned": bool(house.is_banned),
            "floor_ratio": (
                house.floor_no / house.all_floors
                if house.floor_no and house.all_floors
                else None
            ),
            "has_location": house.lat_lng is not None,
            "region_code": house.gu_nm,
        }
