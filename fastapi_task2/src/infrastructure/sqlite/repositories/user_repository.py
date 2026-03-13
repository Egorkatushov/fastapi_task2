from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.user import User
from ....schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self):
        self.model = User

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        return session.get(self.model, user_id)

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        return session.query(self.model).filter(self.model.username == username).first()


    def get_by_email(self, session: Session, email: str) -> Optional[User]:
        return session.query(self.model).filter(self.model.email == email).first()

    def get_all(self, session: Session) -> List[User]:
        return session.query(self.model).all()

    def create(self, session: Session, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        from datetime import datetime

        user = self.model(
            username=user_data.username,
            email=user_data.email or "",
            password=user_data.password,
            first_name=user_data.first_name or "",
            last_name=user_data.last_name or "",
            is_active=user_data.is_active,
            is_superuser=False,
            is_staff=False,
            date_joined=datetime.now(),
            last_login=None
        )
        session.add(user)
        session.flush()
        return user

    def delete(self, session: Session, user_id: int) -> bool:
        """Удалить пользователя по ID"""
        user = self.get_by_id(session, user_id)
        if user:
            session.delete(user)
            return True
        return False

    def update(self, session: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновить данные пользователя"""
        user = self.get_by_id(session, user_id)
        if not user:
            return None

        # Обновляем только переданные поля
        update_data = user_data.model_dump(exclude_unset=True)

        # Поля, которые нельзя обновлять
        forbidden_fields = ['id', 'date_joined']

        for field, value in update_data.items():
            if field not in forbidden_fields and hasattr(user, field):
                # Специальная обработка для email
                if field == 'email' and value == "":
                    setattr(user, field, "")  # пустая строка допустима
                elif value is not None:
                    setattr(user, field, value)

        return user