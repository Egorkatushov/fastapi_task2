from fastapi import APIRouter, Depends, status
from typing import List

from ..schemas.user import User, UserCreate, UserUpdate
from ..domain.user.use_case.get_user import GetUserUseCase
from ..domain.user.use_case.get_users import GetUsersUseCase
from ..domain.user.use_case.create_user import CreateUserUseCase
from ..domain.user.use_case.update_user import UpdateUserUseCase
from ..domain.user.use_case.delete_user import DeleteUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users(
    use_case: GetUsersUseCase = Depends()
) -> List[User]:
    """Получить список всех пользователей"""
    return await use_case.execute()


@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends()
) -> User:
    """Получить пользователя по ID"""
    return await use_case.execute(user_id=user_id)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> User:
    """Создать нового пользователя"""
    return await use_case.execute(user_data=user_data)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> User:
    """Обновить данные пользователя"""
    return await use_case.execute(user_id=user_id, user_data=user_data)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> dict:
    """Удалить пользователя по ID"""
    return await use_case.execute(user_id=user_id)