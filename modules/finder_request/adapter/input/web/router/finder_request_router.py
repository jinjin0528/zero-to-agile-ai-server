from fastapi import APIRouter, Depends, HTTPException, status
from modules.finder_request.adapter.input.web.request.create_finder_request_request import CreateFinderRequestRequest
from modules.finder_request.adapter.input.web.response.finder_request_response import FinderRequestResponse
from modules.finder_request.adapter.input.web.dependencies import get_create_finder_request_usecase
from modules.finder_request.application.usecase.create_finder_request_usecase import CreateFinderRequestUseCase
from modules.finder_request.application.dto.finder_request_dto import CreateFinderRequestDTO


router = APIRouter(prefix="/requests", tags=["Finder Request"])


@router.post(
    "",
    response_model=FinderRequestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="임차인 요구서 생성",
    description="임차인이 자신의 조건이 담긴 요구서를 생성합니다."
)
def create_finder_request(
    request: CreateFinderRequestRequest,
    usecase: CreateFinderRequestUseCase = Depends(get_create_finder_request_usecase)
):
    """
    임차인의 요구서를 생성합니다.
    
    - **abang_user_id**: 임차인 사용자 ID
    - **preferred_region**: 선호 지역
    - **price_type**: 가격 유형 (JEONSE, MONTHLY, MIXED)
    - **max_deposit**: 최대 보증금
    - **max_rent**: 최대 월세
    - **house_type**: 주거 형태
    - **additional_condition**: 추가 조건 (선택)
    """
    try:
        # Web Request DTO → Application DTO 변환
        dto = CreateFinderRequestDTO(
            abang_user_id=request.abang_user_id,
            preferred_region=request.preferred_region,
            price_type=request.price_type,
            max_deposit=request.max_deposit,
            max_rent=request.max_rent,
            house_type=request.house_type,
            additional_condition=request.additional_condition
        )
        
        # UseCase 실행
        result = usecase.execute(dto)
        
        # Application DTO → Web Response DTO 변환
        return FinderRequestResponse(
            finder_request_id=result.finder_request_id,
            abang_user_id=result.abang_user_id,
            preferred_region=result.preferred_region,
            price_type=result.price_type,
            max_deposit=result.max_deposit,
            max_rent=result.max_rent,
            status=result.status,
            house_type=result.house_type,
            additional_condition=result.additional_condition,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"요구서 생성 중 오류가 발생했습니다: {str(e)}"
        )
