from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date


class CreateOwnerHouseRequest(BaseModel):
    """
    임대인 매물 생성 요청
    """
    address: Optional[str] = Field(None, description="매물 주소")
    price_type: Optional[str] = Field(None, description="가격 유형 (JEONSE, MONTHLY, etc)")
    deposit: Optional[int] = Field(None, description="보증금")
    rent: Optional[int] = Field(None, description="월세")
    is_active: bool = Field(True, description="활성 상태 여부")
    open_from: Optional[date] = Field(None, description="오픈 시작일")
    open_to: Optional[date] = Field(None, description="오픈 종료일")
