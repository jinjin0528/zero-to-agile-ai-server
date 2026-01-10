from fastapi import APIRouter, Depends, HTTPException

from infrastructure.db.postgres import get_db_session
from modules.house_analysis.adapter.input.web.request.risk_request import RiskRequest
from modules.house_analysis.adapter.input.web.request.price_request import PriceRequest
from modules.house_analysis.adapter.output.repository.address_codec_repository import (
    AddressCodecRepository,
)
from modules.house_analysis.adapter.output.repository.building_ledger_repository import (
    BuildingLedgerRepository,
)
from modules.house_analysis.adapter.output.repository.price_history_repository import (
    PriceHistoryRepository,
)
from modules.house_analysis.adapter.output.repository.risk_history_repository import (
    RiskHistoryRepository,
)
from modules.house_analysis.adapter.output.repository.transaction_price_repository import (
    TransactionPriceRepository,
)
from modules.house_analysis.application.usecase.analyze_risk_usecase import (
    AnalyzeRiskUseCase,
)
from modules.house_analysis.application.usecase.analyze_price_usecase import (
    AnalyzePriceUseCase,
)
from modules.house_analysis.domain.exception import BuildingInfoNotFoundError

router = APIRouter(prefix="/api/house_analysis")


@router.get("/risk")
def analyze_risk(
    request: RiskRequest = Depends(),
    db_session=Depends(get_db_session),
):
    address_codec_repo = AddressCodecRepository()
    building_ledger_repo = BuildingLedgerRepository()
    risk_history_repo = RiskHistoryRepository(db_session)

    usecase = AnalyzeRiskUseCase(
        address_codec_port=address_codec_repo,
        building_ledger_port=building_ledger_repo,
        risk_history_port=risk_history_repo,
        db_session=db_session,
    )

    try:
        result = usecase.execute(address=request.address)
    except BuildingInfoNotFoundError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {
        "risk_score": result.score,
        "summary": result.summary,
        "comment": result.comment,
    }


@router.get("/price")
def analyze_price(
    request: PriceRequest = Depends(),
    db_session=Depends(get_db_session),
):
    address_codec_repo = AddressCodecRepository()
    transaction_price_repo = TransactionPriceRepository()
    price_history_repo = PriceHistoryRepository(db_session)

    usecase = AnalyzePriceUseCase(
        address_codec_port=address_codec_repo,
        transaction_price_port=transaction_price_repo,
        price_history_port=price_history_repo,
        db_session=db_session,
    )

    result = usecase.execute(
        address=request.address,
        deal_type=request.deal_type,
        property_type=request.property_type,
        price=request.price,
        area=request.area,
    )
    return {
        "price_score": result.score,
        "comment": result.comment,
    }
