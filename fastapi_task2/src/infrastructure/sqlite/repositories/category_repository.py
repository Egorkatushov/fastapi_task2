from typing import Optional, List, Type
from sqlalchemy.orm import Session
from ..models.category import Category


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, category_id: int) -> Optional[Category]:
        return session.query(self._model).filter(self._model.id == category_id).first()

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        return session.query(self._model).filter(self._model.slug == slug).first()

    def get_all(self, session: Session) -> List[Category]:
        return session.query(self._model).all()

    def create(self, session: Session, **kwargs) -> Category:
        category = self._model(**kwargs)
        session.add(category)
        session.flush()
        return category

    def update(self, session: Session, category: Category, **kwargs) -> Category:
        for key, value in kwargs.items():
            if value is not None:
                setattr(category, key, value)
        session.add(category)
        return category

    def delete(self, session: Session, category: Category) -> None:
        session.delete(category)