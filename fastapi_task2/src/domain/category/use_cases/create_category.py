# src/domain/category/use_cases/create_category.py
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....schemas.category import CategoryCreate, Category
from ....core.exceptions.category_exceptions import (
    CategoryNameAlreadyExistsException,
    CategoryAlreadyExistsException  # ← ДОБАВЬТЕ
)
from sqlalchemy.exc import IntegrityError


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> Category:
        with self._database.session() as session:
            # ← ДОБАВЬТЕ ПРОВЕРКУ СУЩЕСТВОВАНИЯ КАТЕГОРИИ ПО ID
            existing_category = self._repo.get(session, category_data.id)
            if existing_category:
                raise CategoryAlreadyExistsException(category_data.id)

            # Проверка уникальности названия
            existing_name = self._repo.get_by_name(session, category_data.name)
            if existing_name:
                raise CategoryNameAlreadyExistsException(category_data.name)

            try:
                category = self._repo.create(session, category_data)
                return Category.model_validate(category)
            except IntegrityError:
                session.rollback()
                raise CategoryAlreadyExistsException(category_data.id)