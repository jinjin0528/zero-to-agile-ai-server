from abc import ABC, abstractmethod
from typing import Optional
from modules.finder_request.domain.finder_request import FinderRequest


class FinderRequestRepositoryPort(ABC):
    """
    FinderRequest Repository의 포트 (인터페이스)
    Application Layer가 의존하는 추상화
    """
    
    @abstractmethod
    def create(self, finder_request: FinderRequest) -> FinderRequest:
        """
        새로운 요구서 생성
        
        Args:
            finder_request: 생성할 요구서 도메인 모델
            
        Returns:
            생성된 요구서 (ID 포함)
        """
        pass
    
    @abstractmethod
    def find_by_id(self, finder_request_id: int) -> Optional[FinderRequest]:
        """
        ID로 요구서 조회
        
        Args:
            finder_request_id: 요구서 ID
            
        Returns:
            요구서 도메인 모델 또는 None
        """
        pass
