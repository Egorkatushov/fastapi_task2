from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.location import Location
from typing import List


class GetLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> List[Location]:
        """Получить список всех локаций"""
        try:
            with self._database.session() as session:
                locations = self._repo.get_all(session)
                return [Location.model_validate(location) for location in locations]

        except Exception as e:
            print(f"Ошибка при получении списка локаций: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )