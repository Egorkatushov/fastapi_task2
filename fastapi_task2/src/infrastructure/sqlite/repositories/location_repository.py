from typing import Optional, List, Type
from sqlalchemy.orm import Session
from..models.location import Location


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, location_id: int) -> Optional[Location]:
        return session.query(self._model).filter(self._model.id == location_id).first()

    def get_by_slug(self, session: Session, slug: str) -> Optional[Location]:
        return session.query(self._model).filter(self._model.slug == slug).first()

    def get_all(self, session: Session) -> List[Location]:
        return session.query(self._model).all()

    def create(self, session: Session, **kwargs) -> Location:
        location = self._model(**kwargs)
        session.add(location)
        session.flush()
        return location

    def update(self, session: Session, location: Location, **kwargs) -> Location:
        for key, value in kwargs.items():
            if value is not None:
                setattr(location, key, value)
        session.add(location)
        return location

    def delete(self, session: Session, location: Location) -> None:
        session.delete(location)