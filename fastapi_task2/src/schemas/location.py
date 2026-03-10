from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LocationBase(BaseModel):
    """Базовая модель локации"""
    name: str = Field(max_length=256)
    description: str | None = None
    slug: str = Field(
        max_length=64,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: bool = True


class LocationCreate(LocationBase):
    """Для создания локации"""
    pass


class LocationUpdate(BaseModel):
    """Для обновления локации"""
    name: str | None = Field(None, max_length=256)
    description: str | None = None
    slug: str | None = Field(None, max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: bool | None = None


class Location(LocationBase):
    """Для чтения локации из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime