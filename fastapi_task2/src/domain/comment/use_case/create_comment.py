from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository
from ....schemas.comment import CommentCreate, Comment


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        with self._database.session() as session:
            # Можно добавить проверку существования поста и автора
            comment = self._repo.create(session, comment_data)
            return Comment.model_validate(comment)