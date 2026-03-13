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
            # Удалена проверка get_by_slug, так как этого метода нет
            location = self._repo.create(session, location_data)
            return Location.model_validate(location)