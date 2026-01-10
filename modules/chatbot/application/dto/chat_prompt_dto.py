from dataclasses import dataclass


@dataclass(frozen=True)
class ChatPromptRequestDto:
    prompt: str


@dataclass(frozen=True)
class ChatPromptResponseDto:
    answer: str
