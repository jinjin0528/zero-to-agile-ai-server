from pydantic import BaseModel, Field


class ChatPromptRequest(BaseModel):
    prompt: str = Field(..., description="프론트에서 전달하는 프롬프트")
