from fastapi import APIRouter, Depends, status
from typing import List, Optional

from ..schemas.post import Post, PostCreate, PostUpdate
from ..domain.post.use_cases.get_post import GetPostUseCase
from ..domain.post.use_cases.get_posts import GetPostsUseCase
from ..domain.post.use_cases.create_post import CreatePostUseCase
from ..domain.post.use_cases.update_post import UpdatePostUseCase
from ..domain.post.use_cases.delete_post import DeletePostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[Post], status_code=status.HTTP_200_OK)
async def get_all_posts(
    category_id: Optional[int] = None,
    location_id: Optional[int] = None,
    author_id: Optional[int] = None,
    use_case: GetPostsUseCase = Depends()
) -> List[Post]:
    """Получить список всех постов с возможностью фильтрации"""
    return await use_case.execute(
        category_id=category_id,
        location_id=location_id,
        author_id=author_id
    )


@router.get("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(
    post_id: int,
    use_case: GetPostUseCase = Depends()
) -> Post:
    """Получить пост по ID"""
    return await use_case.execute(post_id=post_id)


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePostUseCase = Depends()
) -> Post:
    """Создать новый пост"""
    return await use_case.execute(post_data=post_data)


@router.put("/{post_id}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    use_case: UpdatePostUseCase = Depends()
) -> Post:
    """Обновить пост"""
    return await use_case.execute(post_id=post_id, post_data=post_data)


@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(
    post_id: int,
    use_case: DeletePostUseCase = Depends()
) -> dict:
    """Удалить пост по ID"""
    return await use_case.execute(post_id=post_id)