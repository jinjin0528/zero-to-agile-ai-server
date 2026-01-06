from infrastructure.db.postgres import Base
from sqlalchemy import Column, Float, String


class UniversityLocationORM(Base):
    """대학 위치 정보를 조회하기 위한 테이블 매핑."""

    __tablename__ = "university_location"

    university_name = Column(
        String(50), primary_key=True, comment="대학명"
    )
    campus = Column(String(50), primary_key=True, comment="캠퍼스")
    region = Column(String(50), nullable=True, comment="지역")
    road_name_address = Column(
        String(50), nullable=True, comment="도로명 주소"
    )
    jibun_address = Column(String(50), nullable=True, comment="지번 주소")
    lat = Column(Float, nullable=True, comment="위도")
    lng = Column(Float, nullable=True, comment="경도")
