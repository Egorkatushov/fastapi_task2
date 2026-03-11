from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LocationBase(BaseModel):
    """Базовая модель местоположения"""
    name: str = Field(max_length=256)
    is_published: bool = True


class LocationCreate(LocationBase):
    """Для создания новой локации"""
    pass


class LocationUpdate(BaseModel):
    """Для обновления локации - все поля необязательные"""
    name: str | None = Field(None, max_length=256)
    is_published: bool | None = None


class Location(LocationBase):
    """Для чтения локации из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime