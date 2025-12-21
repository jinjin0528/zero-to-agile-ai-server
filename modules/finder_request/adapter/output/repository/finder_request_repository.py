from sqlalchemy.orm import Session
from typing import Optional
from modules.finder_request.application.port.finder_request_repository_port import FinderRequestRepositoryPort
from modules.finder_request.domain.finder_request import FinderRequest
from modules.finder_request.adapter.output.finder_request_model import FinderRequestModel


class FinderRequestRepository(FinderRequestRepositoryPort):
    """
    FinderRequest Repository 구현체
    PostgreSQL을 사용한 영속성 관리
    """
    
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory
    
    def create(self, finder_request: FinderRequest) -> FinderRequest:
        """
        새로운 요구서 생성
        
        Args:
            finder_request: 생성할 요구서 도메인 모델
            
        Returns:
            생성된 요구서 (ID 포함)
        """
        db: Session = self.db_session_factory()
        try:
            # 도메인 모델 → ORM 모델 변환
            model = FinderRequestModel(
                abang_user_id=finder_request.abang_user_id,
                preferred_region=finder_request.preferred_region,
                price_type=finder_request.price_type,
                max_deposit=finder_request.max_deposit,
                max_rent=finder_request.max_rent,
                status=finder_request.status,
                house_type=finder_request.house_type,
                additional_condition=finder_request.additional_condition
            )
            
            db.add(model)
            db.commit()
            db.refresh(model)
            
            # ORM 모델 → 도메인 모델 변환
            return self._to_domain(model)
        finally:
            db.close()
    
    def find_by_id(self, finder_request_id: int) -> Optional[FinderRequest]:
        """
        ID로 요구서 조회
        
        Args:
            finder_request_id: 요구서 ID
            
        Returns:
            요구서 도메인 모델 또는 None
        """
        db: Session = self.db_session_factory()
        try:
            model = db.query(FinderRequestModel).filter(
                FinderRequestModel.finder_request_id == finder_request_id
            ).first()
            
            if not model:
                return None
            
            return self._to_domain(model)
        finally:
            db.close()
    
    def _to_domain(self, model: FinderRequestModel) -> FinderRequest:
        """ORM 모델을 도메인 모델로 변환"""
        return FinderRequest(
            abang_user_id=model.abang_user_id,
            status=model.status,
            finder_request_id=model.finder_request_id,
            preferred_region=model.preferred_region,
            price_type=model.price_type,
            max_deposit=model.max_deposit,
            max_rent=model.max_rent,
            house_type=model.house_type,
            additional_condition=model.additional_condition,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
