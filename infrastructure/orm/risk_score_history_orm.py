from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from infrastructure.db.postgres import Base


class RiskScoreHistory(Base):
    """
    리스크 점수 분석 결과 히스토리 ORM 모델
    - 주소별 리스크 분석 결과를 저장
    """
    __tablename__ = "risk_score_history"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    summary = Column(Integer, nullable=False)
    factors = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
