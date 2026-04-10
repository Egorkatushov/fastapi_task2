from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from typing import List

from ..schemas.location import Location, LocationCreate, LocationUpdate
from ..domain.location.use_cases.get_location import GetLocationUseCase
from ..domain.location.use_cases.get_locations import GetLocationsUseCase
from ..domain.location.use_cases.create_location import CreateLocationUseCase
from ..domain.location.use_cases.update_location import UpdateLocationUseCase
from ..domain.location.use_cases.delete_location import DeleteLocationUseCase
from ..core.exceptions.location_exceptions import (
    LocationNotFoundByIdException,
    LocationNameIsNotUniqueException
)

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[Location], status_code=status.HTTP_200_OK)
async def get_locations(use_case: GetLocationsUseCase = Depends()) -> List[Location]:
    return await use_case.execute()


@router.get("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def get_location(location_id: int, use_case: GetLocationUseCase = Depends()) -> Location:
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post("/", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate, use_case: CreateLocationUseCase = Depends()) -> Location:
    try:
        return await use_case.execute(location_data=location_data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except LocationNameIsNotUniqueException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.put("/{location_id}", response_model=Location, status_code=status.HTTP_200_OK)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_case: UpdateLocationUseCase = Depends()
) -> Location:
    try:
        return await use_case.execute(location_id=location_id, location_data=location_data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    except LocationNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except LocationNameIsNotUniqueException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.delete("/{location_id}", status_code=status.HTTP_200_OK)
async def delete_location(location_id: int, use_case: DeleteLocationUseCase = Depends()) -> dict:
    try:
        return await use_case.execute(location_id=location_id)
    except LocationNotFoundByIdException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())