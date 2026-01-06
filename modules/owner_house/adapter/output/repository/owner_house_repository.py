from typing import List, Optional
from sqlalchemy.orm import Session
from modules.owner_house.domain.owner_house import OwnerHouse
from modules.owner_house.adapter.output.owner_house_model import OwnerHouseModel
from modules.owner_house.application.port.owner_house_repository_port import OwnerHouseRepositoryPort


class OwnerHouseRepository(OwnerHouseRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def save(self, owner_house: OwnerHouse) -> OwnerHouse:
        model = OwnerHouseModel(
            abang_user_id=owner_house.abang_user_id,
            address=owner_house.address,
            price_type=owner_house.price_type,
            deposit=owner_house.deposit,
            rent=owner_house.rent,
            is_active=owner_house.is_active,
            open_from=owner_house.open_from,
            open_to=owner_house.open_to,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def update(self, owner_house: OwnerHouse) -> OwnerHouse:
        model = self.db.query(OwnerHouseModel).filter(
            OwnerHouseModel.owner_house_id == owner_house.owner_house_id
        ).first()

        if model:
            model.address = owner_house.address
            model.price_type = owner_house.price_type
            model.deposit = owner_house.deposit
            model.rent = owner_house.rent
            model.is_active = owner_house.is_active
            model.open_from = owner_house.open_from
            model.open_to = owner_house.open_to
            # abang_user_id is usually not updated
            self.db.commit()
            self.db.refresh(model)
            return self._to_domain(model)
        return None

    def find_by_id(self, owner_house_id: int) -> Optional[OwnerHouse]:
        model = self.db.query(OwnerHouseModel).filter(
            OwnerHouseModel.owner_house_id == owner_house_id
        ).first()
        return self._to_domain(model) if model else None

    def find_all_by_user_id(self, abang_user_id: int) -> List[OwnerHouse]:
        models = self.db.query(OwnerHouseModel).filter(
            OwnerHouseModel.abang_user_id == abang_user_id
        ).all()
        return [self._to_domain(model) for model in models]

    def delete(self, owner_house_id: int) -> bool:
        model = self.db.query(OwnerHouseModel).filter(
            OwnerHouseModel.owner_house_id == owner_house_id
        ).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def _to_domain(self, model: OwnerHouseModel) -> OwnerHouse:
        return OwnerHouse(
            owner_house_id=model.owner_house_id,
            abang_user_id=model.abang_user_id,
            address=model.address,
            price_type=model.price_type,
            deposit=model.deposit,
            rent=model.rent,
            is_active=model.is_active,
            open_from=model.open_from,
            open_to=model.open_to,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
