from typing import List
from modules.owner_house.application.port.owner_house_repository_port import OwnerHouseRepositoryPort
from modules.owner_house.domain.owner_house import OwnerHouse


class ViewOwnerHousesUseCase:
    def __init__(self, repository: OwnerHouseRepositoryPort):
        self.repository = repository

    def execute(self, abang_user_id: int) -> List[OwnerHouse]:
        return self.repository.find_all_by_user_id(abang_user_id)
