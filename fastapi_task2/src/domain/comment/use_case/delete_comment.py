from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.comment_repository import CommentRepository


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> dict:
        with self._database.session() as session:
            deleted = self._repo.delete(session, comment_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with id {comment_id} not found"
                )
            return {"message": f"Comment {comment_id} deleted successfully"}