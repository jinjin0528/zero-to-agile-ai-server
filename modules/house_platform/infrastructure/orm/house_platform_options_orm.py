from sqlalchemy import BigInteger, Boolean, Column, Text
from sqlalchemy.dialects.postgresql import JSONB

from infrastructure.db.postgres import Base


class HousePlatformOptionORM(Base):
    """옵션 정규화 테이블 ORM 매핑."""

    __tablename__ = "house_platform_options"

    house_platform_options_id = Column(
        "house_platform_options_id",
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="옵션 PK",
    )
    house_platform_id = Column(
        BigInteger, nullable=False, comment="매물 FK"
    )
    built_in = Column("built_in", Text, nullable=True, comment="빌트인 옵션(JSON)")
    near_univ = Column(
        "near_univ", Boolean, nullable=True, comment="660m 내 대학 여부"
    )
    near_transport = Column(
        "near_transport", Boolean, nullable=True, comment="660m 내 교통 인접 여부"
    )
    near_mart = Column(
        "near_mart", Boolean, nullable=True, comment="660m 내 편의시설 인접 여부"
    )
    nearby_pois = Column(
        "nearby_pois", JSONB, nullable=True, comment="주변 POI 목록(JSON)"
    )
