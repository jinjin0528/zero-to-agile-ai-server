import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

from modules.house_analysis.adapter.input.web.router import house_analysis_router


class FakeAddressCodecRepository:
    def convert_to_legal_code(self, address: str):
        return {
            "legal_code": "1168010100",
            "address": "서울시 강남구 역삼동"
        }


class FakeBuildingLedgerRepository:
    def fetch_building_info(self, legal_code: str, bun: str, ji: str):
        return {
            "is_violation": True,
            "has_seismic_design": False,
            "building_age": 35,
            "main_use": "생활형숙박시설"
        }


class FakeRiskHistoryRepository:
    def __init__(self, session):
        self.saved_risk_scores = []

    def save(self, risk_score) -> None:
        self.saved_risk_scores.append(risk_score)


class FakeTransactionPriceRepository:
    def fetch_transaction_prices(self, legal_code: str, deal_type: str, property_type: str):
        return [
            {"price": 30000, "area": 30, "deal_type": deal_type}
        ]


class FakePriceHistoryRepository:
    def __init__(self, session):
        self.saved_price_scores = []

    def save(self, price_score) -> None:
        self.saved_price_scores.append(price_score)


class FakeDbSession:
    def commit(self):
        pass

    def rollback(self):
        pass


def _override_get_db_session():
    yield FakeDbSession()


def _create_app(monkeypatch):
    monkeypatch.setattr(
        house_analysis_router,
        "AddressCodecRepository",
        FakeAddressCodecRepository
    )
    monkeypatch.setattr(
        house_analysis_router,
        "BuildingLedgerRepository",
        FakeBuildingLedgerRepository
    )
    monkeypatch.setattr(
        house_analysis_router,
        "RiskHistoryRepository",
        FakeRiskHistoryRepository
    )
    monkeypatch.setattr(
        house_analysis_router,
        "TransactionPriceRepository",
        FakeTransactionPriceRepository
    )
    monkeypatch.setattr(
        house_analysis_router,
        "PriceHistoryRepository",
        FakePriceHistoryRepository
    )

    app = FastAPI()
    app.dependency_overrides[
        house_analysis_router.get_db_session
    ] = _override_get_db_session
    app.include_router(house_analysis_router.router)
    return app


def test_risk_analysis_endpoint_success(monkeypatch):
    """
    GET /api/house_analysis/risk 성공 케이스
    """
    app = _create_app(monkeypatch)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/risk",
        params={"address": "서울시 강남구 역삼동 777-0"}
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["risk_score"] == 100
    assert payload["summary"] == 5
    assert "위반 건축물" in payload["comment"]


def test_risk_analysis_endpoint_validation_error(monkeypatch):
    """
    GET /api/house_analysis/risk 유효성 검증 실패 케이스
    """
    app = _create_app(monkeypatch)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/risk",
        params={"address": ""}
    )

    assert response.status_code == 422


def test_price_analysis_endpoint_success(monkeypatch):
    """
    GET /api/house_analysis/price 성공 케이스
    """
    app = _create_app(monkeypatch)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/price",
        params={
            "address": "서울시 강남구 역삼동 777-0",
            "deal_type": "전세",
            "property_type": "아파트",
            "price": 33000,
            "area": 33
        }
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["price_score"] == 50
    assert payload["comment"] == "동 평균과 비슷한 가격"


def test_price_analysis_endpoint_missing_deal_type(monkeypatch):
    """
    GET /api/house_analysis/price deal_type 누락 케이스
    """
    app = _create_app(monkeypatch)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/price",
        params={
            "address": "서울시 강남구 역삼동 777-0",
            "price": 33000,
            "area": 33
        }
    )

    assert response.status_code == 422


def test_router_dependency_injection(monkeypatch):
    """
    Depends로 주입된 DB 세션이 Repository에 전달되는지 확인
    """
    sentinel_session = FakeDbSession()
    captured = {}

    class CapturingRiskHistoryRepository:
        def __init__(self, session):
            captured["session"] = session

        def save(self, risk_score) -> None:
            pass

    def override_session():
        yield sentinel_session

    current_module = sys.modules[__name__]
    monkeypatch.setattr(
        current_module,
        "FakeRiskHistoryRepository",
        CapturingRiskHistoryRepository
    )
    monkeypatch.setattr(
        current_module,
        "_override_get_db_session",
        override_session
    )

    app = _create_app(monkeypatch)
    client = TestClient(app)

    response = client.get(
        "/api/house_analysis/risk",
        params={"address": "서울시 강남구 역삼동 777-0"}
    )

    assert response.status_code == 200
    assert captured["session"] is sentinel_session
