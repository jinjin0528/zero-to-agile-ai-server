from pydantic import BaseModel, Field
from modules.ai_explanation.domain.tone import ChatTone


# [1] 내 건물 정보
class OwnerHouseData(BaseModel):
    title: str = Field(..., description="매물 이름 (예: 신림동 신축 원룸)")
    monthly_rent: int = Field(..., description="월세 (예: 500000)")
    deposit: int = Field(..., description="보증금 (예: 5000000)")
    address: str = Field(..., description="주소")
    room_type: str = Field(..., description="방 종류 (OPEN=원룸 등)")


# [2] 세입자 후보 정보
class TenantCandidateData(BaseModel):
    finder_request_id: int
    price_type: str = Field(..., description="선호 거래 유형 (MONTHLY 등)")
    max_rent: int = Field(..., description="세입자 최대 월세 예산")
    preferred_region: str = Field(..., description="세입자 선호 지역")
    house_type: str = Field(..., description="세입자 선호 주거 형태")


# 임대인용 설명 요청
class OwnerExplanationRequest(BaseModel):
    tone: ChatTone = Field(default=ChatTone.FORMAL)  # 기본값: 정중한 어조

    # 내 건물 정보
    my_house: OwnerHouseData

    # 추천된 세입자 후보 1명 (리스트 중 사용자가 클릭한 특정 후보)
    finders: TenantCandidateData