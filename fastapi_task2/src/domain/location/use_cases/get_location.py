from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.location import Location


class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        """Получить локацию по ID"""
        try:
            with self._database.session() as session:
                location = self._repo.get(session, location_id)

                if not location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                return Location.model_validate(location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при получении локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )