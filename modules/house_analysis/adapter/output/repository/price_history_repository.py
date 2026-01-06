"""
Price Score History Repository 구현체
"""
from sqlalchemy.orm import Session

from infrastructure.orm.price_score_history_orm import PriceScoreHistory
from modules.house_analysis.application.port.price_history_port import PriceHistoryPort
from modules.house_analysis.domain.model import PriceScore


class PriceHistoryRepository(PriceHistoryPort):
    """
    가격 점수 히스토리를 DB에 저장하는 Repository
    """

    def __init__(self, session: Session):
        """
        Initialize PriceHistoryRepository

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def save(self, price_score: PriceScore) -> None:
        """
        가격 점수를 DB에 저장

        Note: commit은 호출자(UseCase)에서 수행해야 함

        Args:
            price_score: PriceScore 도메인 모델
        """
        history = PriceScoreHistory(
            address=price_score.address,
            deal_type=price_score.metrics.get("deal_type", ""),
            price_score=price_score.score,
            comment=price_score.comment,
            metrics=price_score.metrics
        )

        self.session.add(history)
