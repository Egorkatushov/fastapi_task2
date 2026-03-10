from typing import Optional, List, Type
from sqlalchemy.orm import Session
from ..models.comment import Comment


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, comment_id: int) -> Optional[Comment]:
        return session.query(self._model).filter(self._model.id == comment_id).first()

    def get_by_post(self, session: Session, post_id: int) -> List[Comment]:
        return session.query(self._model).filter(self._model.post_id == post_id).all()

    def create(self, session: Session, **kwargs) -> Comment:
        comment = self._model(**kwargs)
        session.add(comment)
        session.flush()
        return comment

    def update(self, session: Session, comment: Comment, **kwargs) -> Comment:
        for key, value in kwargs.items():
            if value is not None:
                setattr(comment, key, value)
        session.add(comment)
        return comment

    def delete(self, session: Session, comment: Comment) -> None:
        session.delete(comment)