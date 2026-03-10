from typing import Optional, List, Type
from sqlalchemy.orm import Session
from ..models.user import User


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, user_id: int) -> Optional[User]:
        return session.query(self._model).filter(self._model.id == user_id).first()

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        return session.query(self._model).filter(self._model.username == username).first()

    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        return session.query(self._model).filter(self._model.email == email).first()

    def get_all(self, session: Session) -> List[User]:
        return session.query(self._model).all()

    def create(self, session: Session, **kwargs) -> User:
        user = self._model(**kwargs)
        session.add(user)
        session.flush()
        return user

    def update(self, session: Session, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        session.add(user)
        return user

    def delete(self, session: Session, user: User) -> None:
        session.delete(user)