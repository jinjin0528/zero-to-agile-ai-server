from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class CreateOwnerHouseDTO:
    abang_user_id: int
    address: Optional[str]
    price_type: Optional[str]
    deposit: Optional[int]
    rent: Optional[int]
    is_active: bool
    open_from: Optional[date]
    open_to: Optional[date]


@dataclass
class UpdateOwnerHouseDTO:
    owner_house_id: int
    abang_user_id: int  # To verify ownership
    address: Optional[str] = None
    price_type: Optional[str] = None
    deposit: Optional[int] = None
    rent: Optional[int] = None
    is_active: Optional[bool] = None
    open_from: Optional[date] = None
    open_to: Optional[date] = None
