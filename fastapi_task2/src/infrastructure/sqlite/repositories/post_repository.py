from typing import Optional, List, Type
from sqlalchemy.orm import Session
from ..models.post import Post


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, post_id: int) -> Optional[Post]:
        return session.query(self._model).filter(self._model.id == post_id).first()

    def get_all(
            self,
            session: Session,
            category_id: Optional[int] = None,
            location_id: Optional[int] = None,
            author_id: Optional[int] = None
    ) -> List[Post]:
        query = session.query(self._model)

        if category_id is not None:
            query = query.filter(self._model.category_id == category_id)
        if location_id is not None:
            query = query.filter(self._model.location_id == location_id)
        if author_id is not None:
            query = query.filter(self._model.author_id == author_id)

        return query.all()

    def create(self, session: Session, **kwargs) -> Post:
        post = self._model(**kwargs)
        session.add(post)
        session.flush()
        return post

    def update(self, session: Session, post: Post, **kwargs) -> Post:
        for key, value in kwargs.items():
            if value is not None:
                setattr(post, key, value)
        session.add(post)
        return post

    def delete(self, session: Session, post: Post) -> None:
        session.delete(post)