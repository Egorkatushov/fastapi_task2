from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository
from ....schemas.comment import CommentCreate, Comment


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        """Создать новый комментарий"""
        try:
            with self._database.session() as session:
                # Здесь можно добавить проверки существования post_id и author_id
                new_comment = self._repo.create(session, **comment_data.model_dump())
                return Comment.model_validate(new_comment)

        except Exception as e:
            print(f"Ошибка при создании комментария: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )