from modules.chatbot.application.dto.chat_prompt_dto import (
    ChatPromptRequestDto,
    ChatPromptResponseDto,
)
from modules.chatbot.application.port_in.chat_prompt_port import ChatPromptPort
from modules.chatbot.application.port_out.llm_port import LLMPort


class GenerateChatResponseUseCase(ChatPromptPort):
    def __init__(self, llm_port: LLMPort) -> None:
        self._llm_port = llm_port

    def execute(self, request: ChatPromptRequestDto) -> ChatPromptResponseDto:
        answer = self._llm_port.generate(request.prompt)
        return ChatPromptResponseDto(answer=answer)
