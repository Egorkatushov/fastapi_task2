from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....schemas.user import UserCreate, User
from datetime import datetime


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        try:
            with self._database.session() as session:
                # Проверяем уникальность username
                existing_username = self._repo.get_by_username(session, user_data.username)
                if existing_username:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Пользователь с username '{user_data.username}' уже существует"
                    )

                # Проверяем уникальность email
                existing_email = self._repo.get_by_email(session, user_data.email)
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Пользователь с email '{user_data.email}' уже существует"
                    )

                # Создаем пользователя со всеми полями Django
                new_user = self._repo.create(
                    session=session,
                    username=user_data.username,
                    email=user_data.email,
                    password=user_data.password,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                    is_active=user_data.is_active,
                    is_staff=user_data.is_staff,
                    is_superuser=user_data.is_superuser,
                    date_joined=datetime.now(),
                    last_login=None
                )

                return User.model_validate(new_user)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )