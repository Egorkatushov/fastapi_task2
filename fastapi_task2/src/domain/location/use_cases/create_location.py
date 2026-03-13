from fastapi import HTTPException, status
from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.location import LocationCreate, Location


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        with self._database.session() as session:
            # Проверяем, не существует ли уже локация с таким ID
            existing = self._repo.get(session, location_data.id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Location with id {location_data.id} already exists"
                )

            location = self._repo.create(session, location_data)
            return Location.model_validate(location)