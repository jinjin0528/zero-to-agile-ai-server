from fastapi import Depends
from infrastructure.db.postgres import get_db_session
from modules.owner_house.adapter.output.repository.owner_house_repository import OwnerHouseRepository
from modules.owner_house.application.usecase.create_owner_house_usecase import CreateOwnerHouseUseCase
from modules.owner_house.application.usecase.view_owner_houses_usecase import ViewOwnerHousesUseCase
from modules.owner_house.application.usecase.get_owner_house_detail_usecase import GetOwnerHouseDetailUseCase
from modules.owner_house.application.usecase.edit_owner_house_usecase import EditOwnerHouseUseCase
from modules.owner_house.application.usecase.delete_owner_house_usecase import DeleteOwnerHouseUseCase

def get_owner_house_repository(db_session=Depends(get_db_session)):
    return OwnerHouseRepository(db_session)

def get_create_owner_house_usecase(
    repository: OwnerHouseRepository = Depends(get_owner_house_repository)
):
    return CreateOwnerHouseUseCase(repository)

def get_view_owner_houses_usecase(
    repository: OwnerHouseRepository = Depends(get_owner_house_repository)
):
    return ViewOwnerHousesUseCase(repository)

def get_get_owner_house_detail_usecase(
    repository: OwnerHouseRepository = Depends(get_owner_house_repository)
):
    return GetOwnerHouseDetailUseCase(repository)

def get_edit_owner_house_usecase(
    repository: OwnerHouseRepository = Depends(get_owner_house_repository)
):
    return EditOwnerHouseUseCase(repository)

def get_delete_owner_house_usecase(
    repository: OwnerHouseRepository = Depends(get_owner_house_repository)
):
    return DeleteOwnerHouseUseCase(repository)