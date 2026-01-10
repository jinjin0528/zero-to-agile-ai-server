from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class HousePlatform:
    house_platform_id: Optional[int]
    title: Optional[str]
    address: Optional[str]
    deposit: Optional[int]
    domain_id: Optional[int]
    rgst_no: Optional[str]
    sales_type: Optional[str]
    monthly_rent: Optional[int]
    room_type: Optional[str]
    contract_area: Optional[float]
    exclusive_area: Optional[float]
    floor_no: Optional[int]
    all_floors: Optional[int]
    lat_lng: Optional[Dict[str, Any]]
    manage_cost: Optional[int]
    can_park: Optional[bool]
    has_elevator: Optional[bool]
    image_urls: Optional[str]
    pnu_cd: Optional[str]
    is_banned: Optional[bool]
    residence_type: Optional[str]
    gu_nm: Optional[str]
    dong_nm: Optional[str]
    registered_at: Optional[datetime]
    crawled_at: Optional[datetime]
    snapshot_id: Optional[str]
    abang_user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
