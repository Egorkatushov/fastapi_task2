from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.user import User
from ....schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self):
        self.model = User

    def get(self, session: Session, user_id: int) -> Optional[User]:
        return session.get(self.model, user_id)

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        return self.get(session, user_id)

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        return session.query(self.model).filter(self.model.username == username).first()

    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        return session.query(self.model).filter(self.model.email == email).first()

    def get_all(self, session: Session) -> List[User]:
        return session.query(self.model).all()

    def create(self, session: Session, user_data: UserCreate) -> User:
        """Создать нового пользователя с указанным ID"""
        user = self.model(
            id=user_data.id,
            username=user_data.username,
            email=user_data.email or "",
            password=user_data.password,
            first_name=user_data.first_name or "",
            last_name=user_data.last_name or "",
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser,
            is_staff=user_data.is_staff,
            date_joined=user_data.date_joined,
            last_login=user_data.last_login
        )
        session.add(user)
        session.flush()
        return user

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get(session, user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        forbidden_fields = ['id', 'date_joined']

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(user, field):
                if value is not None:
                    setattr(user, field, value)

        return user

    def delete(self, session: Session, user_id: int) -> bool:
        user = self.get(session, user_id)
        if user:
            session.delete(user)
            return True
        return False