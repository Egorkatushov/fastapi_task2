from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....schemas.category import Category
from typing import List


class GetCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> List[Category]:
        """Получить список всех категорий"""
        try:
            with self._database.session() as session:
                categories = self._repo.get_all(session)
                return [Category.model_validate(category) for category in categories]

        except Exception as e:
            print(f"Ошибка при получении списка категорий: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )