from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from modules.auth.adapter.input.auth_middleware import auth_required
from modules.owner_house.adapter.input.web.request.create_owner_house_request import CreateOwnerHouseRequest
from modules.owner_house.adapter.input.web.request.update_owner_house_request import UpdateOwnerHouseRequest
from modules.owner_house.adapter.input.web.response.owner_house_response import OwnerHouseResponse
from modules.owner_house.application.dto.owner_house_dto import CreateOwnerHouseDTO, UpdateOwnerHouseDTO
from modules.owner_house.application.usecase.create_owner_house_usecase import CreateOwnerHouseUseCase
from modules.owner_house.application.usecase.view_owner_houses_usecase import ViewOwnerHousesUseCase
from modules.owner_house.application.usecase.get_owner_house_detail_usecase import GetOwnerHouseDetailUseCase
from modules.owner_house.application.usecase.edit_owner_house_usecase import EditOwnerHouseUseCase
from modules.owner_house.application.usecase.delete_owner_house_usecase import DeleteOwnerHouseUseCase
from modules.owner_house.adapter.input.web.dependencies import (
    get_create_owner_house_usecase,
    get_view_owner_houses_usecase,
    get_get_owner_house_detail_usecase,
    get_edit_owner_house_usecase,
    get_delete_owner_house_usecase
)

router = APIRouter(prefix="/owner_houses", tags=["Owner House"])


@router.post(
    "/create",
    response_model=OwnerHouseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="임대인 매물 등록",
    description="임대인이 새로운 매물을 등록합니다."
)
def create_owner_house(
    request: CreateOwnerHouseRequest,
    abang_user_id: int = Depends(auth_required),
    usecase: CreateOwnerHouseUseCase = Depends(get_create_owner_house_usecase)
):
    """
    임대인 매물을 등록합니다.
    """
    try:
        dto = CreateOwnerHouseDTO(
            abang_user_id=abang_user_id,
            address=request.address,
            price_type=request.price_type,
            deposit=request.deposit,
            rent=request.rent,
            is_active=request.is_active,
            open_from=request.open_from,
            open_to=request.open_to
        )
        
        result = usecase.execute(dto)
        
        return OwnerHouseResponse(
            owner_house_id=result.owner_house_id,
            abang_user_id=result.abang_user_id,
            address=result.address,
            price_type=result.price_type,
            deposit=result.deposit,
            rent=result.rent,
            is_active=result.is_active,
            open_from=result.open_from,
            open_to=result.open_to,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"매물 등록 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/view",
    response_model=List[OwnerHouseResponse],
    summary="임대인 매물 목록 조회",
    description="본인이 등록한 매물 목록을 조회합니다."
)
def view_owner_houses(
    abang_user_id: int = Depends(auth_required),
    usecase: ViewOwnerHousesUseCase = Depends(get_view_owner_houses_usecase)
):
    """
    본인이 등록한 매물 목록을 조회합니다.
    """
    try:
        results = usecase.execute(abang_user_id)
        
        return [
            OwnerHouseResponse(
                owner_house_id=result.owner_house_id,
                abang_user_id=result.abang_user_id,
                address=result.address,
                price_type=result.price_type,
                deposit=result.deposit,
                rent=result.rent,
                is_active=result.is_active,
                open_from=result.open_from,
                open_to=result.open_to,
                created_at=result.created_at,
                updated_at=result.updated_at
            )
            for result in results
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"매물 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get(
    "/view/{owner_house_id}",
    response_model=OwnerHouseResponse,
    summary="임대인 매물 상세 조회",
    description="특정 매물의 상세 정보를 조회합니다."
)
def get_owner_house_detail(
    owner_house_id: int,
    usecase: GetOwnerHouseDetailUseCase = Depends(get_get_owner_house_detail_usecase)
):
    """
    매물 상세 정보를 조회합니다.
    """
    try:
        result = usecase.execute(owner_house_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"매물 ID {owner_house_id}를 찾을 수 없습니다."
            )
            
        return OwnerHouseResponse(
            owner_house_id=result.owner_house_id,
            abang_user_id=result.abang_user_id,
            address=result.address,
            price_type=result.price_type,
            deposit=result.deposit,
            rent=result.rent,
            is_active=result.is_active,
            open_from=result.open_from,
            open_to=result.open_to,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"매물 상세 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.put(
    "/edit",
    response_model=OwnerHouseResponse,
    summary="임대인 매물 수정",
    description="본인이 등록한 매물을 수정합니다."
)
def edit_owner_house(
    request: UpdateOwnerHouseRequest,
    abang_user_id: int = Depends(auth_required),
    usecase: EditOwnerHouseUseCase = Depends(get_edit_owner_house_usecase)
):
    """
    본인이 등록한 매물을 수정합니다.
    """
    try:
        dto = UpdateOwnerHouseDTO(
            owner_house_id=request.owner_house_id,
            abang_user_id=abang_user_id,
            address=request.address,
            price_type=request.price_type,
            deposit=request.deposit,
            rent=request.rent,
            is_active=request.is_active,
            open_from=request.open_from,
            open_to=request.open_to
        )
        
        result = usecase.execute(dto)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="매물을 찾을 수 없거나 수정 권한이 없습니다."
            )
            
        return OwnerHouseResponse(
            owner_house_id=result.owner_house_id,
            abang_user_id=result.abang_user_id,
            address=result.address,
            price_type=result.price_type,
            deposit=result.deposit,
            rent=result.rent,
            is_active=result.is_active,
            open_from=result.open_from,
            open_to=result.open_to,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"매물 수정 중 오류가 발생했습니다: {str(e)}"
        )


@router.delete(
    "/delete",
    summary="임대인 매물 삭제",
    description="본인이 등록한 매물을 삭제합니다."
)
def delete_owner_house(
    owner_house_id: int = Query(..., description="삭제할 매물 ID", gt=0),
    abang_user_id: int = Depends(auth_required),
    usecase: DeleteOwnerHouseUseCase = Depends(get_delete_owner_house_usecase)
):
    """
    본인이 등록한 매물을 삭제합니다.
    """
    try:
        success = usecase.execute(owner_house_id, abang_user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="매물을 찾을 수 없거나 삭제 권한이 없습니다."
            )
            
        return {"message": "매물이 성공적으로 삭제되었습니다.", "owner_house_id": owner_house_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"매물 삭제 중 오류가 발생했습니다: {str(e)}"
        )
