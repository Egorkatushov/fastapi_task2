from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....schemas.user import User
from typing import List


class GetUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> List[User]:
        """Получить список всех пользователей"""
        try:
            with self._database.session() as session:
                users = self._repo.get_all(session)
                return [User.model_validate(user) for user in users]

        except Exception as e:
            print(f"Ошибка при получении списка пользователей: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )