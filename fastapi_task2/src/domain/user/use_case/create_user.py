# src/domain/user/use_case/create_user.py
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....schemas.user import UserCreate, User
from ....core.exceptions.user_exceptions import (
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException,  # ← правильное имя (IsNotUnique, а не AlreadyExists)
    UserAlreadyExistsException
)
from sqlalchemy.exc import IntegrityError


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        with self._database.session() as session:
            # Проверка существования пользователя по ID
            existing_user = self._repo.get(session, user_data.id)
            if existing_user:
                raise UserAlreadyExistsException(user_data.id)

            # Проверка уникальности username
            existing_username = self._repo.get_by_username(session, user_data.username)
            if existing_username:
                raise UserUsernameIsNotUniqueException(user_data.username)

            # Проверка уникальности email
            existing_email = self._repo.get_by_email(session, user_data.email)
            if existing_email:
                raise UserEmailIsNotUniqueException(user_data.email)  # ← правильное имя

            try:
                user = self._repo.create(session, user_data)
                return User.model_validate(user)
            except IntegrityError:
                session.rollback()
                raise UserAlreadyExistsException(user_data.id)