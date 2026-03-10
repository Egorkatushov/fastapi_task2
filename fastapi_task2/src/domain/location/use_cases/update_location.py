from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.location import LocationUpdate, Location


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int, location_data: LocationUpdate) -> Location:
        """Обновить локацию"""
        try:
            with self._database.session() as session:
                # Проверяем существование локации
                location = self._repo.get(session, location_id)
                if not location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Локация с ID {location_id} не найдена"
                    )

                # Проверяем уникальность slug, если он меняется
                if location_data.slug and location_data.slug != location.slug:
                    existing_slug = self._repo.get_by_slug(session, location_data.slug)
                    if existing_slug:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Локация со slug '{location_data.slug}' уже существует"
                        )

                # Обновляем локацию
                update_data = location_data.model_dump(exclude_unset=True)
                updated_location = self._repo.update(session, location, **update_data)

                return Location.model_validate(updated_location)

        except HTTPException:
            raise
        except Exception as e:
            print(f"Ошибка при обновлении локации: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Внутренняя ошибка сервера"
            )