from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from typing import List, Optional

from ..schemas.post import Post, PostCreate, PostUpdate
from ..domain.post.use_cases.get_post import GetPostUseCase
from ..domain.post.use_cases.get_posts import GetPostsUseCase
from ..domain.post.use_cases.create_post import CreatePostUseCase
from ..domain.post.use_cases.update_post import UpdatePostUseCase
from ..domain.post.use_cases.delete_post import DeletePostUseCase
from ..core.exceptions.post_exceptions import (
    PostNotFoundByIdException,
    PostAuthorNotFoundException,
    PostCategoryNotFoundException,
    PostLocationNotFoundException,
    PostAlreadyExistsException
)
from ..core.exceptions.user_exceptions import UserNotFoundByIdException as UserNotFoundEx
from ..core.exceptions.category_exceptions import CategoryNotFoundByIdException
from ..core.exceptions.location_exceptions import LocationNotFoundByIdException

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[Post], status_code=status.HTTP_200_OK)
async def get_posts(
    category_id: Optional[int] = None,
    location_id: Optional[int] = None,
    author_id: Optional[int] = None,
    use_case: GetPostsUseCase = Depends()
) -> List[Post]:
    return await use_case.execute(category_id=category_id, location_id=location_id, author_id=author_id)


@router.get("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, use_case: GetPostUseCase = Depends()) -> Post:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, use_case: CreatePostUseCase = Depends()) -> Post:
    try:
        return await use_case.execute(post_data=post_data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except PostAlreadyExistsException as e:  # ← ДОБАВЬТЕ ЭТОТ БЛОК
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())
    except (UserNotFoundEx, PostAuthorNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except (CategoryNotFoundByIdException, PostCategoryNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except (LocationNotFoundByIdException, PostLocationNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    use_case: UpdatePostUseCase = Depends()
) -> Post:
    try:
        return await use_case.execute(post_id=post_id, post_data=post_data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except PostNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, use_case: DeletePostUseCase = Depends()) -> dict:
    try:
        return await use_case.execute(post_id=post_id)
    except PostNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())