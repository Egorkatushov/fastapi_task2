from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....schemas.category import CategoryUpdate, Category


class UpdateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int, category_data: CategoryUpdate) -> Category:
        """Обновить категорию"""
        try:
            with self._database.session() as session:
                # Проверяем существование категории
                category = self._repo.get(session, category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                # Проверяем уникальность slug, если он меняется
                if category_data.slug and category_data.slug != category.slug:
                    existing_slug = self._repo.get_by_slug(session, category_data.slug)
                    if existing_slug:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Категория со slug '{category_data.slug}' уже существует"
                        )

                # Обновляем категорию
                update_data = category_data.model_dump(exclude_unset=True)
                updated_category = self._repo.update(session, category, **update_data)

                return Category.model_validate(updated_category)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )