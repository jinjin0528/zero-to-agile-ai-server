from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class UpdateOwnerHouseRequest(BaseModel):
    """
    임대인 매물 수정 요청
    """
    owner_house_id: int = Field(..., description="수정할 매물 ID")
    address: Optional[str] = Field(None, description="매물 주소")
    price_type: Optional[str] = Field(None, description="가격 유형")
    deposit: Optional[int] = Field(None, description="보증금")
    rent: Optional[int] = Field(None, description="월세")
    is_active: Optional[bool] = Field(None, description="활성 상태 여부")
    open_from: Optional[date] = Field(None, description="오픈 시작일")
    open_to: Optional[date] = Field(None, description="오픈 종료일")
