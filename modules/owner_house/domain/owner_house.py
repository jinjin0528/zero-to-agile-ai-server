from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class OwnerHouse:
    """
    임대인(owner)의 보유 매물(house)을 나타내는 도메인 모델
    """
    abang_user_id: int
    owner_house_id: Optional[int] = None
    address: Optional[str] = None
    price_type: Optional[str] = None  # e.g., JEONSE, MONTHLY
    deposit: Optional[int] = None
    rent: Optional[int] = None
    is_active: bool = True
    open_from: Optional[date] = None
    open_to: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def deactivate(self):
        """매물을 비활성화"""
        self.is_active = False

    def activate(self):
        """매물을 활성화"""
        self.is_active = True
