from fastapi import APIRouter, Depends, status
from typing import List

from ..schemas.user import User, UserCreate, UserUpdate
from ..domain.user.use_case.get_user import GetUserUseCase
from ..domain.user.use_case.get_users import GetUsersUseCase
from ..domain.user.use_case.create_user import CreateUserUseCase
from ..domain.user.use_case.update_user import UpdateUserUseCase
from ..domain.user.use_case.delete_user import DeleteUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    operation_id="users_get_all"  # Уникальное имя
)
async def get_all_users(
    use_case: GetUsersUseCase = Depends()
) -> List[User]:
    return await use_case.execute()


@router.get(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    operation_id="users_get_one"  # Уникальное имя
)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends()
) -> User:
    return await use_case.execute(user_id=user_id)


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    operation_id="users_create"  # Уникальное имя
)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> User:
    return await use_case.execute(user_data=user_data)


@router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    operation_id="users_update"  # Уникальное имя
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> User:
    return await use_case.execute(user_id=user_id, user_data=user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    operation_id="users_delete"  # Уникальное имя
)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> dict:
    return await use_case.execute(user_id=user_id)