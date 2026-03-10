from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository
from ....schemas.category import CategoryCreate, Category


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_data: CategoryCreate) -> Category:
        """Создать новую категорию"""
        try:
            with self._database.session() as session:
                # Проверяем уникальность slug
                existing_slug = self._repo.get_by_slug(session, category_data.slug)
                if existing_slug:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Категория со slug '{category_data.slug}' уже существует"
                    )

                # Создаем категорию
                new_category = self._repo.create(session, **category_data.model_dump())

                return Category.model_validate(new_category)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )