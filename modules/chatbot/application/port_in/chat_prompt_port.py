from abc import ABC, abstractmethod

from modules.chatbot.application.dto.chat_prompt_dto import (
    ChatPromptRequestDto,
    ChatPromptResponseDto,
)


class ChatPromptPort(ABC):
    @abstractmethod
    def execute(self, request: ChatPromptRequestDto) -> ChatPromptResponseDto:
        raise NotImplementedError
