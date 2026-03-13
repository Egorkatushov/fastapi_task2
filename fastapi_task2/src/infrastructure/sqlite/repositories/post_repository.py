from typing import Optional, List, Type
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.post import Post
from ....schemas.post import PostCreate, PostUpdate


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

    def create(self, session: Session, post_data: PostCreate) -> Post:
        """Создать новый пост с указанным ID"""
        post = self._model(
            id=post_data.id,
            title=post_data.title,
            text=post_data.text,
            pub_date=post_data.pub_date,
            author_id=post_data.author_id,
            category_id=post_data.category_id,
            location_id=post_data.location_id,
            image=post_data.image,
            is_published=post_data.is_published,
            created_at=post_data.created_at
        )
        session.add(post)
        session.flush()
        return post

    def update(self, session: Session, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        post = self.get(session, post_id)
        if not post:
            return None

        update_data = post_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None and hasattr(post, key):
                setattr(post, key, value)

        session.add(post)
        return post

    def delete(self, session: Session, post_id: int) -> bool:
        post = self.get(session, post_id)
        if post:
            session.delete(post)
            return True
        return False