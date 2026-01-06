import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.house_analysis.adapter.output.repository.address_codec_repository import AddressCodecRepository
from modules.house_analysis.adapter.output.repository.building_ledger_repository import BuildingLedgerRepository
from modules.house_analysis.adapter.output.repository.transaction_price_repository import TransactionPriceRepository
from modules.house_analysis.adapter.output.repository.risk_history_repository import RiskHistoryRepository
from modules.house_analysis.adapter.output.repository.price_history_repository import PriceHistoryRepository
from modules.house_analysis.domain.model import RiskScore, PriceScore
from infrastructure.orm.risk_score_history_orm import RiskScoreHistory
from infrastructure.orm.price_score_history_orm import PriceScoreHistory
from infrastructure.db.postgres import Base


def test_address_codec_repository_integration():
    """
    실제 주소 → 법정동 코드 변환 테스트
    - AddressCodecRepository의 convert_to_legal_code() 메서드 테스트
    - 실제 변환 로직 또는 Mock 데이터 사용
    """
    # Given: AddressCodecRepository 인스턴스
    repository = AddressCodecRepository()

    # When: 주소를 법정동 코드로 변환
    result = repository.convert_to_legal_code("서울시 강남구 역삼동 777-0")

    # Then: 법정동 코드와 주소 정보가 반환됨
    assert result is not None
    assert "legal_code" in result
    assert "address" in result
    assert len(result["legal_code"]) > 0
    assert "역삼동" in result["address"] or "강남구" in result["address"]


def test_building_ledger_repository_integration():
    """
    실제 건축물대장 API 호출 테스트
    - BuildingLedgerRepository의 fetch_building_info() 메서드 테스트
    - 실제 API 호출 또는 Mock 데이터 사용
    """
    # Given: BuildingLedgerRepository 인스턴스
    repository = BuildingLedgerRepository()

    # When: 법정동 코드로 건축물 정보 조회
    result = repository.fetch_building_info("1168010100", "0777", "0000")

    # Then: 건축물 정보가 반환됨
    assert result is not None
    assert "is_violation" in result
    assert "has_seismic_design" in result
    assert "building_age" in result
    assert "main_use" in result
    assert isinstance(result["is_violation"], bool)
    assert isinstance(result["has_seismic_design"], bool)
    assert isinstance(result["building_age"], int)


def test_transaction_price_repository_integration():
    """
    실제 실거래가 API 호출 테스트
    - TransactionPriceRepository의 fetch_transaction_prices() 메서드 테스트
    - 실제 API 호출 또는 Mock 데이터 사용
    """
    # Given: TransactionPriceRepository 인스턴스
    repository = TransactionPriceRepository()

    # When: 법정동 코드와 거래 유형으로 실거래가 조회
    result = repository.fetch_transaction_prices("1168010100", "전세", "아파트")

    # Then: 실거래가 목록이 반환됨
    assert result is not None
    assert isinstance(result, list)
    # 데이터가 있을 수도 없을 수도 있지만, 리스트 형태여야 함
    if len(result) > 0:
        assert "price" in result[0]
        assert "area" in result[0]
        assert "deal_type" in result[0]


def test_risk_history_repository_save():
    """
    RiskHistoryRepository의 save() 메서드 테스트
    - 실제 DB 또는 in-memory DB 사용
    """
    # Given: in-memory SQLite DB 설정
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Given: RiskHistoryRepository와 RiskScore 도메인 모델
    repository = RiskHistoryRepository(session)
    risk_score = RiskScore(
        score=75,
        factors={
            "is_violation": False,
            "has_seismic_design": False,
            "building_age": 25
        },
        summary=4,
        comment="내진 설계 미적용",
        address="서울시 강남구 역삼동 777-0"
    )

    # When: RiskScore를 DB에 저장
    repository.save(risk_score)
    session.flush()  # flush to generate ID for SQLite

    # Then: DB에 저장되었는지 확인
    saved = session.query(RiskScoreHistory).first()
    assert saved is not None
    assert saved.address == "서울시 강남구 역삼동 777-0"
    assert saved.risk_score == 75
    assert saved.summary == 4
    assert saved.factors["is_violation"] is False
    assert saved.factors["has_seismic_design"] is False
    assert saved.factors["building_age"] == 25

    # Cleanup
    session.close()


def test_price_history_repository_save():
    """
    PriceHistoryRepository의 save() 메서드 테스트
    - 실제 DB 또는 in-memory DB 사용
    """
    # Given: in-memory SQLite DB 설정
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Given: PriceHistoryRepository와 PriceScore 도메인 모델
    repository = PriceHistoryRepository(session)
    price_score = PriceScore(
        score=38,
        comment="동 평균 대비 약 22% 높은 가격",
        metrics={
            "price_per_area": 1200,
            "area_average": 983,
            "diff_percent": 22,
            "deal_type": "전세"
        },
        address="서울시 강남구 역삼동 777-0"
    )

    # When: PriceScore를 DB에 저장
    repository.save(price_score)
    session.flush()

    # Then: DB에 저장되었는지 확인
    saved = session.query(PriceScoreHistory).first()
    assert saved is not None
    assert saved.address == "서울시 강남구 역삼동 777-0"
    assert saved.deal_type == "전세"
    assert saved.price_score == 38
    assert saved.comment == "동 평균 대비 약 22% 높은 가격"
    assert saved.metrics["price_per_area"] == 1200
    assert saved.metrics["area_average"] == 983
    assert saved.metrics["diff_percent"] == 22

    # Cleanup
    session.close()
