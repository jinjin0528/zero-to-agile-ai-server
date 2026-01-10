from fastapi import APIRouter
from modules.ai_explanation.adapter.input.web.request.owner_request import OwnerExplanationRequest
from modules.ai_explanation.adapter.input.web.response.ai_response import AiResponse
from modules.ai_explanation.application.usecase.explain_owner_usecase import ExplainOwnerUseCase

router = APIRouter(tags=["AI Explanation (Owner)"])

@router.post("/owner", response_model=AiResponse)
def explain_for_owner(request: OwnerExplanationRequest):
    usecase = ExplainOwnerUseCase()
    return usecase.execute(request)