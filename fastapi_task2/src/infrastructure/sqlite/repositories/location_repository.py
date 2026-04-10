from typing import Optional, List, Type
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.location import Location
from ....schemas.location import LocationCreate, LocationUpdate


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, location_id: int) -> Optional[Location]:
        return session.query(self._model).filter(self._model.id == location_id).first()

    def get_by_name(self, session: Session, name: str) -> Optional[Location]:
        """Получить локацию по имени"""
        return session.query(self._model).filter(self._model.name == name).first()

    def get_all(self, session: Session) -> List[Location]:
        return session.query(self._model).all()

    def create(self, session: Session, location_data: LocationCreate) -> Location:
        """Создать новую локацию с указанным ID"""
        location = self._model(
            id=location_data.id,
            name=location_data.name,
            is_published=location_data.is_published,
            created_at=location_data.created_at
        )
        session.add(location)
        session.flush()
        return location

    def update(self, session: Session, location_id: int, location_data: LocationUpdate) -> Optional[Location]:
        location = self.get(session, location_id)
        if not location:
            return None

        update_data = location_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(location, field):
                setattr(location, field, value)

        session.add(location)
        return location

    def delete(self, session: Session, location_id: int) -> bool:
        location = self.get(session, location_id)
        if location:
            session.delete(location)
            return True
        return False