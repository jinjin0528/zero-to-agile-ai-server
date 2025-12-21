from fastapi import Depends
from infrastructure.db.postgres import get_db_session
from modules.finder_request.adapter.output.repository.finder_request_repository import FinderRequestRepository
from modules.finder_request.application.usecase.create_finder_request_usecase import CreateFinderRequestUseCase


def get_finder_request_repository(db_session_factory=Depends(get_db_session)):
    """FinderRequest Repository 인스턴스 생성"""
    return FinderRequestRepository(db_session_factory)


def get_create_finder_request_usecase(
    repository: FinderRequestRepository = Depends(get_finder_request_repository)
) -> CreateFinderRequestUseCase:
    """CreateFinderRequest UseCase 인스턴스 생성"""
    return CreateFinderRequestUseCase(repository)
