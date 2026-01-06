from sqlalchemy import BigInteger, Column, DateTime, Text, func

from infrastructure.db.postgres import Base


class HousePlatformManagementORM(Base):
    """관리비 포함/제외 테이블 ORM 매핑."""

    __tablename__ = "house_platform_management"

    house_platform_management_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="관리비 PK",
    )
    house_platform_id = Column(
        BigInteger, nullable=False, comment="매물 FK"
    )
    management_included = Column(
        Text, nullable=True, comment="관리비 포함 항목(JSON)"
    )
    management_excluded = Column(
        Text, nullable=True, comment="관리비 제외 항목(JSON)"
    )
    created_at = Column(
        DateTime, server_default=func.now(), nullable=True, comment="생성 시각"
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
        comment="수정 시각",
    )
