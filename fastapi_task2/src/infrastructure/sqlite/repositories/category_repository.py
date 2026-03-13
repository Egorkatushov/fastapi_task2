from typing import Optional, List, Type
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.category import Category
from ....schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, category_id: int) -> Optional[Category]:
        return session.query(self._model).filter(self._model.id == category_id).first()

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        return session.query(self._model).filter(self._model.slug == slug).first()

    def get_all(self, session: Session) -> List[Category]:
        return session.query(self._model).all()

    def create(self, session: Session, category_data: CategoryCreate) -> Category:
        """Создать новую категорию с указанным ID"""
        category = self._model(
            id=category_data.id,
            title=category_data.title,
            description=category_data.description,
            slug=category_data.slug,
            is_published=category_data.is_published,
            created_at=category_data.created_at
        )
        session.add(category)
        session.flush()
        return category

    def update(self, session: Session, category_id: int, category_data: CategoryUpdate) -> Optional[Category]:
        category = self.get(session, category_id)
        if not category:
            return None

        update_data = category_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(category, field):
                setattr(category, field, value)

        session.add(category)
        return category

    def delete(self, session: Session, category_id: int) -> bool:
        category = self.get(session, category_id)
        if category:
            session.delete(category)
            return True
        return False