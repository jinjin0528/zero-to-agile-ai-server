from abc import ABC, abstractmethod
from typing import List, Optional
from modules.owner_house.domain.owner_house import OwnerHouse


class OwnerHouseRepositoryPort(ABC):
    @abstractmethod
    def save(self, owner_house: OwnerHouse) -> OwnerHouse:
        """매물 정보를 저장 (Create)"""
        pass

    @abstractmethod
    def update(self, owner_house: OwnerHouse) -> OwnerHouse:
        """매물 정보를 수정 (Update)"""
        pass

    @abstractmethod
    def find_by_id(self, owner_house_id: int) -> Optional[OwnerHouse]:
        """ID로 매물 조회 (Read Detail)"""
        pass

    @abstractmethod
    def find_all_by_user_id(self, abang_user_id: int) -> List[OwnerHouse]:
        """사용자 ID로 모든 매물 조회 (Read List)"""
        pass

    @abstractmethod
    def delete(self, owner_house_id: int) -> bool:
        """매물 삭제 (Delete)"""
        pass
