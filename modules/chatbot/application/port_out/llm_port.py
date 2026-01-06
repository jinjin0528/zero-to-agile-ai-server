from abc import ABC, abstractmethod


class LLMPort(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError
