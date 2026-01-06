from typing import Optional
from modules.owner_house.application.port.owner_house_repository_port import OwnerHouseRepositoryPort
from modules.owner_house.application.dto.owner_house_dto import UpdateOwnerHouseDTO
from modules.owner_house.domain.owner_house import OwnerHouse


class EditOwnerHouseUseCase:
    def __init__(self, repository: OwnerHouseRepositoryPort):
        self.repository = repository

    def execute(self, dto: UpdateOwnerHouseDTO) -> Optional[OwnerHouse]:
        existing_house = self.repository.find_by_id(dto.owner_house_id)
        
        # Check existence and ownership
        if not existing_house or existing_house.abang_user_id != dto.abang_user_id:
            return None

        # Update fields if provided
        if dto.address is not None:
            existing_house.address = dto.address
        if dto.price_type is not None:
            existing_house.price_type = dto.price_type
        if dto.deposit is not None:
            existing_house.deposit = dto.deposit
        if dto.rent is not None:
            existing_house.rent = dto.rent
        if dto.is_active is not None:
            existing_house.is_active = dto.is_active
        if dto.open_from is not None:
            existing_house.open_from = dto.open_from
        if dto.open_to is not None:
            existing_house.open_to = dto.open_to

        return self.repository.update(existing_house)
