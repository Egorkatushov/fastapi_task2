from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from typing import List

from ..schemas.user import User, UserCreate, UserUpdate
from ..domain.user.use_case.get_user import GetUserUseCase
from ..domain.user.use_case.get_users import GetUsersUseCase
from ..domain.user.use_case.create_user import CreateUserUseCase
from ..domain.user.use_case.update_user import UpdateUserUseCase
from ..domain.user.use_case.delete_user import DeleteUserUseCase
from ..core.exceptions.user_exceptions import (
    UserNotFoundByIdException,
    UserUsernameIsNotUniqueException,
    UserEmailIsNotUniqueException,
    UserAlreadyExistsException
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    operation_id="users_get_all"
)
async def get_all_users(
    use_case: GetUsersUseCase = Depends()
) -> List[User]:
    return await use_case.execute()


@router.get(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    operation_id="users_get_one"
)
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends()
) -> User:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    operation_id="users_create"
)
async def create_user(
    user_data: UserCreate,
    use_case: CreateUserUseCase = Depends()
) -> User:
    try:
        return await use_case.execute(user_data=user_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except UserAlreadyExistsException as e:  # ← ДОБАВЬТЕ ЭТОТ БЛОК
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )
    except (UserUsernameIsNotUniqueException, UserEmailIsNotUniqueException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )


@router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    operation_id="users_update"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    use_case: UpdateUserUseCase = Depends()
) -> User:
    try:
        return await use_case.execute(user_id=user_id, user_data=user_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except UserNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )
    except (UserUsernameIsNotUniqueException, UserEmailIsNotUniqueException) as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.get_detail()
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    operation_id="users_delete"
)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends()
) -> dict:
    try:
        return await use_case.execute(user_id=user_id)
    except UserNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.get_detail()
        )