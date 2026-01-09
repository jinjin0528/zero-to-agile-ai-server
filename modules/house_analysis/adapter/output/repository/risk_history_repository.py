"""
Risk Score History Repository 구현체
"""
from sqlalchemy.orm import Session
from modules.house_analysis.application.port.risk_history_port import RiskHistoryPort
from modules.house_analysis.domain.model import RiskScore
from infrastructure.orm.risk_score_history_orm import RiskScoreHistory


class RiskHistoryRepository(RiskHistoryPort):
    """
    리스크 점수 히스토리를 DB에 저장하는 Repository
    """

    def __init__(self, session: Session):
        """
        Initialize RiskHistoryRepository

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def save(self, risk_score: RiskScore) -> None:
        """
        리스크 점수를 DB에 저장

        Note: commit은 호출자(UseCase)에서 수행해야 함

        Args:
            risk_score: RiskScore 도메인 모델
        """
        # RiskScore 도메인 모델을 ORM 모델로 변환
        history = RiskScoreHistory(
            address=risk_score.address,
            risk_score=risk_score.score,
            summary=risk_score.summary,
            factors=risk_score.factors
        )

        # DB 세션에 추가 (commit은 호출자가 수행)
        self.session.add(history)
