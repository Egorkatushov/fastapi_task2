from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository
from ....infrastructure.sqlite.repositories.user_repository import UserRepository
from ....infrastructure.sqlite.repositories.post_repository import PostRepository
from ....schemas.comment import CommentCreate, Comment
from ....core.exceptions.comment_exceptions import (
    CommentAuthorNotFoundException,
    CommentPostNotFoundException,
    CommentAlreadyExistsException  # ← ДОБАВЬТЕ ЭТОТ ИМПОРТ
)
from sqlalchemy.exc import IntegrityError  # ← ДОБАВЬТЕ ЭТОТ ИМПОРТ


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(self, comment_data: CommentCreate) -> Comment:
        with self._database.session() as session:
            # ← ДОБАВЬТЕ ПРОВЕРКУ СУЩЕСТВОВАНИЯ КОММЕНТАРИЯ
            existing_comment = self._repo.get(session, comment_data.id)
            if existing_comment:
                raise CommentAlreadyExistsException(comment_data.id)

            author = self._user_repo.get(session, comment_data.author_id)
            if not author:
                raise CommentAuthorNotFoundException(comment_data.author_id)

            post = self._post_repo.get(session, comment_data.post_id)
            if not post:
                raise CommentPostNotFoundException(comment_data.post_id)

            try:
                comment = self._repo.create(session, comment_data)
                return Comment.model_validate(comment)
            except IntegrityError:
                session.rollback()
                raise CommentAlreadyExistsException(comment_data.id)