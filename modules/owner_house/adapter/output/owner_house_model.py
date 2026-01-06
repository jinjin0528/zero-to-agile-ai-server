from sqlalchemy import Column, BigInteger, Integer, String, Boolean, Date, DateTime, func
from infrastructure.db.postgres import Base


class OwnerHouseModel(Base):
    """
    owner_house 테이블 ORM 모델
    임대인의 매물 정보를 저장
    """
    __tablename__ = "owner_house"

    owner_house_id = Column(BigInteger, primary_key=True, autoincrement=True)
    abang_user_id = Column(BigInteger, nullable=False)
    address = Column(String, nullable=True)
    price_type = Column(String(20), nullable=True)
    deposit = Column(BigInteger, nullable=True)
    rent = Column(BigInteger, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
    open_from = Column(Date, nullable=True)
    open_to = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())
