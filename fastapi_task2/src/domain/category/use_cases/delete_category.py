from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.category_repository import CategoryRepository


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> dict:
        """Удалить категорию по ID"""
        try:
            with self._database.session() as session:
                # Проверяем существование категории
                category = self._repo.get(session, category_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Категория с ID {category_id} не найдена"
                    )

                # Удаляем категорию
                self._repo.delete(session, category)

                return {"message": f"Категория с ID {category_id} успешно удалена"}

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при удалении категории: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )