"""
Risk Analysis Service.

This module provides the application service for risk analysis,
coordinating building and transaction data retrieval with risk evaluation.
"""
from typing import List
from modules.risk_analysis.domain.model import BuildingInfo, TransactionInfo, RiskScore
from modules.risk_analysis.domain.rules import (
    ViolationCheckRule,
    SeismicDesignRule,
    BuildingAgeRule,
    PriceDeviationRule,
    RiskEvaluator
)


class RiskAnalysisService:
    """
    Application service for risk analysis.

    This service coordinates the entire risk analysis workflow:
    1. Create building and transaction information
    2. Evaluate risk using domain rules
    3. Return comprehensive risk score

    For MVP, this is simplified to work with direct BuildingInfo and TransactionInfo objects.
    In production, this would fetch data from external APIs.
    """

    def analyze_property(
        self,
        building: BuildingInfo,
        transaction: TransactionInfo,
        property_id: str,
        historical_transactions: List[TransactionInfo] = None
    ) -> RiskScore:
        """
        Analyze risk for a property.

        Args:
            building: Building information
            transaction: Current transaction information
            property_id: Unique identifier for the property
            historical_transactions: List of historical transactions for price comparison

        Returns:
            RiskScore: Comprehensive risk assessment

        Raises:
            ValueError: If property_id is empty
        """
        # Validate input
        if not property_id or property_id.strip() == "":
            raise ValueError("Property ID cannot be empty")

        # Use empty list if no historical transactions provided
        if historical_transactions is None:
            historical_transactions = []

        # Set up risk evaluation rules
        rules = [
            ViolationCheckRule(),
            SeismicDesignRule(),
            BuildingAgeRule(),
            PriceDeviationRule(historical_transactions)
        ]

        # Evaluate risk
        evaluator = RiskEvaluator(rules)
        risk_score = evaluator.evaluate(building, transaction, property_id)

        return risk_score
