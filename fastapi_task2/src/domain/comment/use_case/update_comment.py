from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository
from ....schemas.comment import CommentUpdate, Comment


class UpdateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int, comment_data: CommentUpdate) -> Comment:
        """Обновить комментарий"""
        try:
            with self._database.session() as session:
                # Проверяем существование комментария
                comment = self._repo.get(session, comment_id)
                if not comment:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Комментарий с ID {comment_id} не найден"
                    )

                # Обновляем комментарий
                update_data = comment_data.model_dump(exclude_unset=True)
                updated_comment = self._repo.update(session, comment, **update_data)

                return Comment.model_validate(updated_comment)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении комментария: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )