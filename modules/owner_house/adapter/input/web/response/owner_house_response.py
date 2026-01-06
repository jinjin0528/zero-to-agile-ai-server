from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class OwnerHouseResponse(BaseModel):
    """
    임대인 매물 응답 모델
    """
    owner_house_id: int
    abang_user_id: int
    address: Optional[str]
    price_type: Optional[str]
    deposit: Optional[int]
    rent: Optional[int]
    is_active: bool
    open_from: Optional[date]
    open_to: Optional[date]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
