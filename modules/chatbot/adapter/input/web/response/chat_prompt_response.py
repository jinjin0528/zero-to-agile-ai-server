from pydantic import BaseModel, Field


class ChatPromptResponse(BaseModel):
    answer: str = Field(..., description="GPT 응답")
