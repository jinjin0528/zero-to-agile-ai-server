from abc import ABC, abstractmethod
from typing import Optional, List
from modules.house_platform.domain.house_platform import HousePlatform

class HousePlatformRepository(ABC):
    @abstractmethod
    def save(self, house_platform: HousePlatform) -> HousePlatform:
        pass

    @abstractmethod
    def find_by_id(self, house_platform_id: int) -> Optional[HousePlatform]:
        pass

    @abstractmethod
    def find_all_by_user_id(self, abang_user_id: int) -> List[HousePlatform]:
        pass
        
    @abstractmethod
    def delete(self, house_platform_id: int) -> bool:
        pass
