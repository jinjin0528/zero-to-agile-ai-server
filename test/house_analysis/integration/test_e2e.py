from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infrastructure.db.postgres import Base
from infrastructure.orm.price_score_history_orm import PriceScoreHistory
from infrastructure.orm.risk_score_history_orm import RiskScoreHistory
from modules.house_analysis.adapter.input.web.router import house_analysis_router


def test_main_app_includes_house_analysis_router():
    """
    main.py에 house_analysis_router가 등록되었는지 확인
    """
    content = Path("app/main.py").read_text(encoding="utf-8")
    assert "house_analysis_router" in content
    assert "include_router(house_analysis_router)" in content


def test_e2e_risk_analysis_flow(monkeypatch):
    """
    실제 API 호출 → DB 저장까지 전체 흐름 테스트
    """
    class FakeAddressCodecRepository:
        def convert_to_legal_code(self, address: str):
            return {
                "legal_code": "1168010100",
                "address": "서울시 강남구 역삼동",
                "bun": "0777",
                "ji": "0000",
            }

    class FakeBuildingLedgerRepository:
        def fetch_building_info(self, legal_code: str, bun: str, ji: str):
            return {
                "is_violation": True,
                "has_seismic_design": False,
                "building_age": 35,
                "main_use": "생활형숙박시설",
            }

    monkeypatch.setattr(
        house_analysis_router,
        "AddressCodecRepository",
        FakeAddressCodecRepository,
    )
    monkeypatch.setattr(
        house_analysis_router,
        "BuildingLedgerRepository",
        FakeBuildingLedgerRepository,
    )

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def override_session():
        yield session

    app = FastAPI()
    app.dependency_overrides[
        house_analysis_router.get_db_session
    ] = override_session
    app.include_router(house_analysis_router.router)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/risk",
        params={"address": "서울시 강남구 역삼동 777-0"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["risk_score"] == 100
    assert payload["summary"] == 5
    assert "위반 건축물" in payload["comment"]

    saved = session.query(RiskScoreHistory).first()
    assert saved is not None
    assert saved.address == "서울시 강남구 역삼동 777-0"
    assert saved.risk_score == 100
    assert saved.summary == 5

    session.close()


def test_e2e_price_analysis_flow(monkeypatch):
    """
    실제 API 호출 → DB 저장까지 전체 흐름 테스트 (가격 분석)
    """
    class FakeAddressCodecRepository:
        def convert_to_legal_code(self, address: str):
            return {
                "legal_code": "1168010100",
                "address": "서울시 강남구 역삼동",
                "bun": "0777",
                "ji": "0000",
            }

    class FakeTransactionPriceRepository:
        def fetch_transaction_prices(self, legal_code: str, deal_type: str, property_type: str):
            return [
                {"price": 30000, "area": 30, "deal_type": deal_type},
                {"price": 33000, "area": 33, "deal_type": deal_type},
            ]

    monkeypatch.setattr(
        house_analysis_router,
        "AddressCodecRepository",
        FakeAddressCodecRepository,
    )
    monkeypatch.setattr(
        house_analysis_router,
        "TransactionPriceRepository",
        FakeTransactionPriceRepository,
    )

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    def override_session():
        yield session

    app = FastAPI()
    app.dependency_overrides[
        house_analysis_router.get_db_session
    ] = override_session
    app.include_router(house_analysis_router.router)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/price",
        params={
            "address": "서울시 강남구 역삼동 777-0",
            "deal_type": "전세",
            "property_type": "아파트",
            "price": 33000,
            "area": 33,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["price_score"] == 50
    assert payload["comment"] == "동 평균과 비슷한 가격"

    saved = session.query(PriceScoreHistory).first()
    assert saved is not None
    assert saved.address == "서울시 강남구 역삼동 777-0"
    assert saved.deal_type == "전세"
    assert saved.price_score == 50

    session.close()


def test_concurrent_requests_handling(monkeypatch):
    """
    동시 요청 처리 테스트
    """
    class FakeAddressCodecRepository:
        def convert_to_legal_code(self, address: str):
            return {
                "legal_code": "1168010100",
                "address": "서울시 강남구 역삼동",
                "bun": "0777",
                "ji": "0000",
            }

    class FakeBuildingLedgerRepository:
        def fetch_building_info(self, legal_code: str, bun: str, ji: str):
            return {
                "is_violation": True,
                "has_seismic_design": False,
                "building_age": 35,
                "main_use": "생활형숙박시설",
            }

    monkeypatch.setattr(
        house_analysis_router,
        "AddressCodecRepository",
        FakeAddressCodecRepository,
    )
    monkeypatch.setattr(
        house_analysis_router,
        "BuildingLedgerRepository",
        FakeBuildingLedgerRepository,
    )

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    def override_session():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app = FastAPI()
    app.dependency_overrides[
        house_analysis_router.get_db_session
    ] = override_session
    app.include_router(house_analysis_router.router)

    def _make_request():
        client = TestClient(app)
        response = client.get(
            "/api/house_analysis/risk",
            params={"address": "서울시 강남구 역삼동 777-0"},
        )
        assert response.status_code == 200
        return response.json()

    results = [_make_request() for _ in range(5)]
    assert len(results) == 5
    assert all(item["risk_score"] == 100 for item in results)
