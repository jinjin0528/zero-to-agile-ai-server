from fastapi import APIRouter

from modules.ai_explaination.adapter.input.web.request.recommendation_explaination import (
    RecommendationExplainationRequest,
)
from modules.ai_explaination.application.usecase.explain_recommendation_usecase import (
    ExplainRecommendationUseCase,
)

router = APIRouter(prefix="/ai_explaination", tags=["ai_explaination"])

# [임차인용] 매물 추천 설명
@router.post(
    "/finder",
    response_model=RecommendationExplainationRequest,
)
# todo:  임차인 설명 함수 수정
def explain_recommendation(
    request: RecommendationExplainationRequest,
) -> RecommendationChatbotResponse:
    usecase = ExplainRecommendationUseCase()
    return usecase.execute(request)

# todo [임대인용] 임차인 추천 설명
@router.post(
    "/owner",
    response_model=RecommendationExplainationRequest,
)
def explain_tenant_recommendation(
    request: LandlordRecommendationRequest, # 임대인용 요청 모델(함수 추가)
):
    usecase = ExplainRecommendationUseCase()
    return usecase.execute_for_landlord(request) # 메서드 명시적 분리