from fastapi import APIRouter
from modules.ai_explanation.adapter.input.web.request.finder_request import FinderExplanationRequest
from modules.ai_explanation.adapter.input.web.response.ai_response import AiResponse
from modules.ai_explanation.application.usecase.explain_finder_usecase import ExplainFinderUseCase

# prefix는 main.py 등에서 통합할 때 "/explain"으로 잡거나 여기서 잡음
router = APIRouter(tags=["AI Explanation (Finder)"])

@router.post("/finder", response_model=AiResponse)
def explain_for_finder(request: FinderExplanationRequest):
    usecase = ExplainFinderUseCase()
    return usecase.execute(request)