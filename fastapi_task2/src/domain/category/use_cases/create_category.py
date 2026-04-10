# src/domain/category/use_cases/create_category.py
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....schemas.category import CategoryCreate, Category
from ....core.exceptions.category_exceptions import (
    CategoryNameAlreadyExistsException,
    CategoryAlreadyExistsException,
    CategoryTitleEmptyException,
    CategoryDescriptionEmptyException,
    CategorySlugEmptyException
)
from sqlalchemy.exc import IntegrityError


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> Category:
        # Валидация на пустые значения
        if not category_data.title or not category_data.title.strip():
            raise CategoryTitleEmptyException()

        if not category_data.description or not category_data.description.strip():
            raise CategoryDescriptionEmptyException()

        if not category_data.slug or not category_data.slug.strip():
            raise CategorySlugEmptyException()

        with self._database.session() as session:
            # Проверка существования категории по ID
            existing_category = self._repo.get(session, category_data.id)
            if existing_category:
                raise CategoryAlreadyExistsException(category_data.id)

            # Проверка уникальности названия
            existing_title = self._repo.get_by_title(session, category_data.title)
            if existing_title:
                raise CategoryNameAlreadyExistsException(category_data.title)

            try:
                category = self._repo.create(session, category_data)
                return Category.model_validate(category)
            except IntegrityError:
                session.rollback()
                raise CategoryAlreadyExistsException(category_data.id)