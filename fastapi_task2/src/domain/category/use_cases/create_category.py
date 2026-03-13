from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....schemas.category import CategoryCreate, Category


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> Category:
        with self._database.session() as session:
            # Проверка уникальности slug
            existing = self._repo.get_by_slug(session, category_data.slug)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with slug '{category_data.slug}' already exists"
                )
            # Передаем всю схему, а не отдельные поля
            category = self._repo.create(session, category_data)
            return Category.model_validate(category)