import pytest
from modules.house_analysis.domain.model import RiskScore
from modules.house_analysis.domain.service import (
    calculate_risk_score,
    generate_risk_summary,
    generate_risk_comment,
)


def test_risk_score_domain_model_creation():
    """
    RiskScore 도메인 모델 생성 테스트
    - score, factors, summary 필드를 가진 dataclass
    - 기본값 설정 확인
    """
    # Given: 리스크 점수 데이터
    score = 72
    factors = {"violation": True, "seismic_design": False, "building_age": 30}
    summary = 4
    comment = "내진 설계 미적용"

    # When: RiskScore 도메인 모델 생성
    risk_score = RiskScore(
        score=score,
        factors=factors,
        summary=summary,
        comment=comment,
        address="서울시 강남구 역삼동 777-0"
    )

    # Then: 모델이 올바르게 생성되고 값이 저장됨
    assert risk_score.score == 72
    assert risk_score.factors == {"violation": True, "seismic_design": False, "building_age": 30}
    assert risk_score.summary == 4
    assert risk_score.comment == "내진 설계 미적용"


def test_calculate_risk_score_with_violation():
    """
    위반 건축물인 경우 리스크 점수 계산 테스트
    - 위반 여부가 True이면 점수 +30
    """
    # Given: 위반 건축물 정보
    building_info = {
        "is_violation": True,
        "has_seismic_design": True,
        "building_age": 5,
        "main_use": "단독주택"
    }

    # When: 리스크 점수 계산
    score = calculate_risk_score(building_info)

    # Then: 위반(+45) + 노후도(5년 이하 +0) = 45점
    assert score == 45


def test_calculate_risk_score_without_seismic_design():
    """
    내진 설계 없는 경우 리스크 점수 계산 테스트
    - 내진 설계가 False이면 점수 +25
    """
    # Given: 내진 설계가 없는 건축물 정보
    building_info = {
        "is_violation": False,
        "has_seismic_design": False,
        "building_age": 5,
        "main_use": "단독주택"
    }

    # When: 리스크 점수 계산
    score = calculate_risk_score(building_info)

    # Then: 내진 미적용(+10) + 노후도(5년 이하 +0) = 10점
    assert score == 10


def test_calculate_risk_score_by_building_age():
    """
    건물 노후도에 따른 리스크 점수 계산 테스트
    - 30년 이상: +20점
    - 20~29년: +14점
    - 10~19년: +8점
    - 5~9년: +4점
    - 5년 이하: +0점
    """
    # Given & When & Then: 30년 이상 건물
    building_info_30_plus = {
        "is_violation": False,
        "has_seismic_design": True,
        "building_age": 35,
        "main_use": "단독주택"
    }
    score_30_plus = calculate_risk_score(building_info_30_plus)
    assert score_30_plus == 20

    # Given & When & Then: 20~30년 건물
    building_info_20_to_30 = {
        "is_violation": False,
        "has_seismic_design": True,
        "building_age": 25,
        "main_use": "단독주택"
    }
    score_20_to_30 = calculate_risk_score(building_info_20_to_30)
    assert score_20_to_30 == 14

    # Given & When & Then: 10~20년 건물
    building_info_10_to_20 = {
        "is_violation": False,
        "has_seismic_design": True,
        "building_age": 15,
        "main_use": "단독주택"
    }
    score_10_to_20 = calculate_risk_score(building_info_10_to_20)
    assert score_10_to_20 == 8

    # Given & When & Then: 10년 미만 건물
    building_info_under_10 = {
        "is_violation": False,
        "has_seismic_design": True,
        "building_age": 5,
        "main_use": "단독주택"
    }
    score_under_10 = calculate_risk_score(building_info_under_10)
    assert score_under_10 == 0

    # Given & When & Then: 5~9년 건물
    building_info_5_to_9 = {
        "is_violation": False,
        "has_seismic_design": True,
        "building_age": 7,
        "main_use": "단독주택"
    }
    score_5_to_9 = calculate_risk_score(building_info_5_to_9)
    assert score_5_to_9 == 4


def test_calculate_risk_score_combined():
    """
    여러 요소가 결합된 리스크 점수 계산 테스트
    - 위반 건축물 + 내진 미적용 + 30년 이상 + 주용도 매우 위험 = 100점
    """
    # Given: 모든 위험 요소를 가진 건축물
    building_info = {
        "is_violation": True,
        "has_seismic_design": False,
        "building_age": 35,
        "main_use": "생활형숙박시설"
    }

    # When: 리스크 점수 계산
    score = calculate_risk_score(building_info)

    # Then: 모든 요소가 합산되어 100점
    assert score == 100  # 45 + 10 + 20 + 25


def test_generate_risk_summary_message():
    """
    리스크 점수에 따른 요약 메시지 생성 테스트
    - 점수 범위별 적절한 메시지 반환
    """
    # Given & When & Then: 0-19점
    assert generate_risk_summary(10) == 1

    # Given & When & Then: 20-39점
    assert generate_risk_summary(25) == 2

    # Given & When & Then: 40-59점
    assert generate_risk_summary(45) == 3

    # Given & When & Then: 60-79점
    assert generate_risk_summary(72) == 4

    # Given & When & Then: 80-100점
    assert generate_risk_summary(95) == 5


def test_generate_risk_comment():
    """
    리스크 요인 코멘트 생성 테스트
    """
    building_info = {
        "is_violation": True,
        "has_seismic_design": False,
        "building_age": 35,
        "main_use": "생활형숙박시설",
    }
    comment = generate_risk_comment(building_info)
    assert "위반 건축물" in comment
    assert "내진 설계 미적용" in comment
    assert "30년 이상 노후" in comment
    assert "생활형숙박시설" in comment
