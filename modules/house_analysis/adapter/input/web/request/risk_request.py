from pydantic import BaseModel, Field


class RiskRequest(BaseModel):
    """리스크 분석 요청 DTO (Query)"""
    address: str = Field(..., min_length=1)
