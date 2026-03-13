from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....schemas.user import UserCreate, User


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        with self._database.session() as session:
            # Проверка уникальности username
            existing_username = self._repo.get_by_username(session, user_data.username)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User with username '{user_data.username}' already exists"
                )

            # Создание пользователя
            user = self._repo.create(session, user_data)
            return User.model_validate(user)