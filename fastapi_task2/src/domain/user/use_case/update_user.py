from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....schemas.user import UserUpdate, User


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, user_data: UserUpdate) -> User:
        """Обновить данные пользователя"""
        try:
            with self._database.session() as session:
                # Проверяем существование пользователя
                user = self._repo.get(session, user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Пользователь с ID {user_id} не найден"
                    )

                # Проверяем уникальность username, если он меняется
                if user_data.username and user_data.username != user.username:
                    existing_username = self._repo.get_by_username(session, user_data.username)
                    if existing_username:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с username '{user_data.username}' уже существует"
                        )

                # Проверяем уникальность email, если он меняется
                if user_data.email and user_data.email != user.email:
                    existing_email = self._repo.get_by_email(session, user_data.email)
                    if existing_email:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Пользователь с email '{user_data.email}' уже существует"
                        )

                # Обновляем пользователя
                update_data = user_data.model_dump(exclude_unset=True)
                updated_user = self._repo.update(session, user, **update_data)

                return User.model_validate(updated_user)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )