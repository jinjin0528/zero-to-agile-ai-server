from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Numeric, func, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from infrastructure.db.postgres import Base

class HousePlatform(Base):
    __tablename__ = "house_platform"

    house_platform_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    address = Column(String, nullable=True)
    deposit = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    domain_id = Column(Integer, default=1)
    rgst_no = Column(String(50), nullable=True)
    sales_type = Column(String(20), nullable=True)
    monthly_rent = Column(BigInteger, nullable=True)
    room_type = Column(String(20), nullable=True)
    contract_area = Column(Numeric(10, 2), nullable=True)
    exclusive_area = Column(Numeric(10, 2), nullable=True)
    floor_no = Column(Integer, nullable=True)
    all_floors = Column(Integer, nullable=True)
    lat_lng = Column(JSONB, nullable=True)
    manage_cost = Column(BigInteger, nullable=True)
    can_park = Column(Boolean, nullable=True)
    has_elevator = Column(Boolean, nullable=True)
    image_urls = Column(String, nullable=True)
    pnu_cd = Column(String, nullable=True)
    is_banned = Column(Boolean, default=False)
    residence_type = Column(String(50), nullable=True)
    gu_nm = Column(String(10), nullable=True)
    dong_nm = Column(String(10), nullable=True)
    registered_at = Column(DateTime, nullable=True)
    crawled_at = Column(DateTime, default=func.now())
    snapshot_id = Column(String(64), nullable=True)
    abang_user_id = Column(BigInteger, nullable=False, default=-1)
