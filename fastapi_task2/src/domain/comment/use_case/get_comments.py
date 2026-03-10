from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository
from ....schemas.comment import Comment
from typing import List


class GetCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, post_id: int) -> List[Comment]:
        """Получить все комментарии к посту"""
        try:
            with self._database.session() as session:
                comments = self._repo.get_by_post(session, post_id)
                return [Comment.model_validate(comment) for comment in comments]

        except Exception as e:
            print(f"Ошибка при получении списка комментариев: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )