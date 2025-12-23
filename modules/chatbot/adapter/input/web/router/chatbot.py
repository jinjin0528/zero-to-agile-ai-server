from fastapi import APIRouter

from modules.chatbot.adapter.input.web.request.recommendation_chatbot import (
    RecommendationChatbotRequest,
)
from modules.chatbot.adapter.input.web.response.recommendation_chatbot import (
    RecommendationChatbotResponse,
)
from modules.chatbot.application.usecase.explain_house_recommendation_usecase import (
    ExplainHouseRecommendationUseCase,
)

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post(
    "/recommendation",
    response_model=RecommendationChatbotResponse,
)
def explain_recommendation(
    request: RecommendationChatbotRequest,
) -> RecommendationChatbotResponse:
    usecase = ExplainHouseRecommendationUseCase()
    return usecase.execute(request)