from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# ==========================================
# [Input] 들어오는 데이터 (User Constraints + Observation)
# ==========================================

# 1. 유저 조건 (query_context['user_constraints'] 매핑)
class UserConstraintsInput(BaseModel):
    budget_deposit_max: Optional[int] = Field(None, description="최대 보증금 (만원)")
    budget_monthly_max: Optional[int] = Field(None, description="최대 월세 (만원)")
    max_commute_min: Optional[int] = Field(None, description="최대 통학 시간 (분)")
    # 필요한 다른 필드들 (washer_yn 등)도 추가 가능

# 2. 매물 성적표 - 가격 (observation_summary['price'] 매핑)
class ObservationPriceInput(BaseModel):
    monthly_cost_est: float = Field(..., description="월 비용 추정치")
    price_percentile: float = Field(..., description="가격 백분위 (0.0~1.0)")
    estimated_move_in_cost: Optional[float] = None

# 3. 매물 성적표 - 통학 (observation_summary['commute'] 매핑)
class ObservationCommuteInput(BaseModel):
    distance_to_school_min: float = Field(..., description="학교 통학 시간(분)")
    distance_bucket: Optional[str] = None
    distance_percentile: Optional[float] = None

# 4. 전체 성적표 묶음
class ObservationSummaryInput(BaseModel):
    price: ObservationPriceInput
    commute: ObservationCommuteInput
    # risk, options 등은 필요시 추가

# [최종 Input] UseCase에 넘길 객체
class ExplanationInput(BaseModel):
    user_constraints: UserConstraintsInput
    observation_summary: ObservationSummaryInput


# ==========================================
# [Output] 나가는 데이터 (JSON 응답 구조)
# ==========================================

class ReasonItem(BaseModel):
    code: str                  # 예: "AFFORDABLE_IN_COHORT"
    text: str                  # 예: "주변 시세 대비 저렴합니다."
    evidence: Dict[str, Any]   # 예: {"price_percentile": 0.22}

class ExplanationResult(BaseModel):
    recommended_reasons: List[ReasonItem] = Field(default_factory=list)
    reject_reasons: List[ReasonItem] = Field(default_factory=list)