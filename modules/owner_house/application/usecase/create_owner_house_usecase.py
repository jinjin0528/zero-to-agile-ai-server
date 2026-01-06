from modules.owner_house.application.port.owner_house_repository_port import OwnerHouseRepositoryPort
from modules.owner_house.application.dto.owner_house_dto import CreateOwnerHouseDTO
from modules.owner_house.domain.owner_house import OwnerHouse


class CreateOwnerHouseUseCase:
    def __init__(self, repository: OwnerHouseRepositoryPort):
        self.repository = repository

    def execute(self, dto: CreateOwnerHouseDTO) -> OwnerHouse:
        owner_house = OwnerHouse(
            abang_user_id=dto.abang_user_id,
            address=dto.address,
            price_type=dto.price_type,
            deposit=dto.deposit,
            rent=dto.rent,
            is_active=dto.is_active,
            open_from=dto.open_from,
            open_to=dto.open_to
        )
        return self.repository.save(owner_house)
