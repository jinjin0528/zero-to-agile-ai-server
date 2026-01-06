from pydantic import BaseModel, Field


class PriceRequest(BaseModel):
    """가격 분석 요청 DTO (Query)"""
    address: str = Field(..., min_length=1)
    deal_type: str = Field(..., min_length=1)
    property_type: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    area: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    area: float = Field(..., gt=0)
