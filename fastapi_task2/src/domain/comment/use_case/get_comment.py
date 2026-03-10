from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository
from ....schemas.comment import Comment


class GetCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        """Получить комментарий по ID"""
        try:
            with self._database.session() as session:
                comment = self._repo.get(session, comment_id)

                if not comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с ID {comment_id} не найден"
                    )

                return Comment.model_validate(comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении комментария: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )