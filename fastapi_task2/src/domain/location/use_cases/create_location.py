from ....infrastructure.sqlite.database import database
from ....infrastructure.sqlite.repositories.location_repository import LocationRepository
from ....schemas.location import LocationCreate, Location
from ....core.exceptions.location_exceptions import LocationNameIsNotUniqueException


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_data: LocationCreate) -> Location:
        with self._database.session() as session:
            existing = self._repo.get_by_name(session, location_data.name)
            if existing:
                raise LocationNameIsNotUniqueException(location_data.name)

            location = self._repo.create(session, location_data)
            return Location.model_validate(location)