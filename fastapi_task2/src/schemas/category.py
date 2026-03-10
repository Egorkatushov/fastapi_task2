from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CategoryBase(BaseModel):
    """Базовая модель категории"""
    title: str = Field(max_length=256)
    description: str
    slug: str = Field(
        max_length=64,
        pattern=r'^[a-zA-Z0-9_-]+$'
    )
    is_published: bool = True


class CategoryCreate(CategoryBase):
    """Для создания категории"""
    pass


class CategoryUpdate(BaseModel):
    """Для обновления категории"""
    title: str | None = Field(None, max_length=256)
    description: str | None = None
    slug: str | None = Field(None, max_length=64, pattern=r'^[a-zA-Z0-9_-]+$')
    is_published: bool | None = None


class Category(CategoryBase):
    """Для чтения категории из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime