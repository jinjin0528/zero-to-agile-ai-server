from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from modules.chatbot.adapter.input.web.request.chat_prompt_request import (
    ChatPromptRequest,
)
from modules.chatbot.adapter.input.web.response.chat_prompt_response import (
    ChatPromptResponse,
)
from modules.chatbot.adapter.output.openai_chat_adapter import OpenAIChatAdapter
from modules.chatbot.application.dto.chat_prompt_dto import ChatPromptRequestDto
from modules.chatbot.application.usecase.generate_chat_response_usecase import (
    GenerateChatResponseUseCase,
)
from shared.common.utils.token_counter import count_tokens
from shared.infrastructure.config.llm_config import LLM_MODEL, MAX_PROMPT_TOKENS

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/prompt", response_model=ChatPromptResponse)
def generate_response(request: ChatPromptRequest) -> ChatPromptResponse:
    token_count = count_tokens(request.prompt, LLM_MODEL)
    if token_count > MAX_PROMPT_TOKENS:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"answer": "너 말이 너무 많아 짧게 말해"},
        )

    usecase = GenerateChatResponseUseCase(llm_port=OpenAIChatAdapter())
    result = usecase.execute(ChatPromptRequestDto(prompt=request.prompt))
    return ChatPromptResponse(answer=result.answer)
