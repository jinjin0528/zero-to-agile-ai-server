from modules.owner_house.application.port.owner_house_repository_port import OwnerHouseRepositoryPort


class DeleteOwnerHouseUseCase:
    def __init__(self, repository: OwnerHouseRepositoryPort):
        self.repository = repository

    def execute(self, owner_house_id: int, abang_user_id: int) -> bool:
        existing_house = self.repository.find_by_id(owner_house_id)
        
        # Check existence and ownership
        if not existing_house or existing_house.abang_user_id != abang_user_id:
            return False

        return self.repository.delete(owner_house_id)
