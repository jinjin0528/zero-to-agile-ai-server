from modules.house_platform.application.port.output.house_platform_repository import HousePlatformRepository

class DeleteHousePlatformUseCase:
    def __init__(self, repository: HousePlatformRepository):
        self.repository = repository

    def execute(self, user_id: int, house_platform_id: int) -> bool:
        existing_house = self.repository.find_by_id(house_platform_id)
        if not existing_house:
            return False
            
        # Permission check
        if existing_house.abang_user_id != user_id:
            raise PermissionError("User is not the owner of this house platform.")
            
        return self.repository.delete(house_platform_id)
