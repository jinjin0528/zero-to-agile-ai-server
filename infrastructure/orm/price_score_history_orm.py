from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from infrastructure.db.postgres import Base


class PriceScoreHistory(Base):
    """
    가격 적정성 점수 분석 결과 히스토리 ORM 모델
    - 주소별 가격 분석 결과를 저장
    """
    __tablename__ = "price_score_history"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    deal_type = Column(String, nullable=False)
    price_score = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    metrics = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
