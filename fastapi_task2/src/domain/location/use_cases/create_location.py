from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.location import LocationCreate, Location


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        """Создать новую локацию"""
        try:
            with self._database.session() as session:
                # Проверяем уникальность slug
                existing_slug = self._repo.get_by_slug(session, location_data.slug)
                if existing_slug:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Локация со slug '{location_data.slug}' уже существует"
                    )

                # Создаем локацию
                new_location = self._repo.create(session, **location_data.model_dump())

                return Location.model_validate(new_location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при создании локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )