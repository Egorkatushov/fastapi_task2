from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class LocationBase(BaseModel):
    name: str = Field(max_length=256)
    is_published: bool = True


class LocationCreate(LocationBase):
    id: int
    created_at: datetime


class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=256)
    is_published: Optional[bool] = None


class Location(LocationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime