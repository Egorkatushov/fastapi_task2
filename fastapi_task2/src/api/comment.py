from fastapi import APIRouter, Depends, status
from typing import List
from fastapi import HTTPException, status

from ..schemas.comment import Comment, CommentCreate, CommentUpdate
from ..domain.comment.use_case.get_comment import GetCommentUseCase
from ..domain.comment.use_case.get_comments import GetCommentsUseCase
from ..domain.comment.use_case.create_comment import CreateCommentUseCase
from ..domain.comment.use_case.update_comment import UpdateCommentUseCase
from ..domain.comment.use_case.delete_comment import DeleteCommentUseCase

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])


@router.get("/", response_model=List[Comment], status_code=status.HTTP_200_OK)
async def get_all_comments(
    post_id: int,
    use_case: GetCommentsUseCase = Depends()
) -> List[Comment]:
    """Получить все комментарии к посту"""
    return await use_case.execute(post_id=post_id)


@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment(
    post_id: int,
    comment_id: int,
    use_case: GetCommentUseCase = Depends()
) -> Comment:
    """Получить комментарий по ID"""
    comment = await use_case.execute(comment_id=comment_id)
    if comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    return comment


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    use_case: CreateCommentUseCase = Depends()
) -> Comment:
    """Создать новый комментарий к посту"""
    # Убедимся, что comment_data.post_id совпадает с post_id из URL
    comment_dict = comment_data.model_dump()
    comment_dict["post_id"] = post_id
    return await use_case.execute(comment_data=CommentCreate(**comment_dict))


@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(
    post_id: int,
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends()
) -> Comment:
    """Обновить комментарий"""
    comment = await use_case.execute(comment_id=comment_id, comment_data=comment_data)
    if comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    post_id: int,
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends()
) -> dict:
    """Удалить комментарий по ID"""
    return await use_case.execute(comment_id=comment_id)