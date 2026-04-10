from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from typing import List

from ..schemas.comment import Comment, CommentCreate, CommentUpdate
from ..domain.comment.use_case.get_comment import GetCommentUseCase
from ..domain.comment.use_case.get_comments import GetCommentsUseCase
from ..domain.comment.use_case.create_comment import CreateCommentUseCase
from ..domain.comment.use_case.update_comment import UpdateCommentUseCase
from ..domain.comment.use_case.delete_comment import DeleteCommentUseCase
from ..core.exceptions.comment_exceptions import (
    CommentNotFoundByIdException,
    CommentAuthorNotFoundException,
    CommentPostNotFoundException,
    CommentAlreadyExistsException  # ← ДОБАВЬТЕ ЭТОТ ИМПОРТ
)
from ..core.exceptions.user_exceptions import UserNotFoundByIdException
from ..core.exceptions.post_exceptions import PostNotFoundByIdException

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])


@router.get("/", response_model=List[Comment], status_code=status.HTTP_200_OK)
async def get_comments(post_id: int, use_case: GetCommentsUseCase = Depends()) -> List[Comment]:
    return await use_case.execute(post_id=post_id)


@router.get("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def get_comment(
    post_id: int,
    comment_id: int,
    use_case: GetCommentUseCase = Depends()
) -> Comment:
    try:
        comment = await use_case.execute(comment_id=comment_id)
        if comment.post_id != post_id:
            raise CommentNotFoundByIdException(comment_id)
        return comment
    except CommentNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    use_case: CreateCommentUseCase = Depends()
) -> Comment:
    try:
        comment_dict = comment_data.model_dump()
        comment_dict["post_id"] = post_id
        return await use_case.execute(comment_data=CommentCreate(**comment_dict))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except CommentAlreadyExistsException as e:  # ← ДОБАВЬТЕ ЭТОТ БЛОК
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())
    except (UserNotFoundByIdException, CommentAuthorNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except (PostNotFoundByIdException, CommentPostNotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put("/{comment_id}", response_model=Comment, status_code=status.HTTP_200_OK)
async def update_comment(
    post_id: int,
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateCommentUseCase = Depends()
) -> Comment:
    try:
        comment = await use_case.execute(comment_id=comment_id, comment_data=comment_data)
        if comment.post_id != post_id:
            raise CommentNotFoundByIdException(comment_id)
        return comment
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except CommentNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    post_id: int,
    comment_id: int,
    use_case: DeleteCommentUseCase = Depends()
) -> dict:
    try:
        return await use_case.execute(comment_id=comment_id)
    except CommentNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())