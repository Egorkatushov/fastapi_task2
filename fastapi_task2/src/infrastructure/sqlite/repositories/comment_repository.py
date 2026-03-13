from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.comment import Comment
from ....schemas.comment import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self):
        self.model = Comment

    def get_by_id(self, session: Session, comment_id: int) -> Optional[Comment]:
        return session.get(self.model, comment_id)

    def get(self, session: Session, comment_id: int) -> Optional[Comment]:
        return self.get_by_id(session, comment_id)

    def get_by_post(self, session: Session, post_id: int) -> List[Comment]:
        return session.query(self.model).filter(self.model.post_id == post_id).all()

    def create(self, session: Session, comment_data: CommentCreate) -> Comment:
        """Создать новый комментарий с указанным ID"""
        comment = self.model(
            id=comment_data.id,
            text=comment_data.text,
            post_id=comment_data.post_id,
            author_id=comment_data.author_id,
            created_at=comment_data.created_at
        )
        session.add(comment)
        session.flush()
        return comment

    def update(self, session: Session, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        comment = self.get_by_id(session, comment_id)
        if not comment:
            return None

        if comment_data.text is not None:
            comment.text = comment_data.text

        session.add(comment)
        return comment

    def delete(self, session: Session, comment_id: int) -> bool:
        comment = self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            return True
        return False