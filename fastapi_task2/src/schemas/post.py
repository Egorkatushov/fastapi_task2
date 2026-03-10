from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    """Базовая модель поста"""
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    author_id: int
    location_id: int | None = None
    category_id: int | None = None
    image: str | None = None
    is_published: bool = True


class PostCreate(PostBase):
    """Для создания поста"""
    pass


class PostUpdate(BaseModel):
    """Для обновления поста"""
    title: str | None = Field(None, max_length=256)
    text: str | None = None
    pub_date: datetime | None = None
    author_id: int | None = None
    location_id: int | None = None
    category_id: int | None = None
    image: str | None = None
    is_published: bool | None = None


class Post(PostBase):
    """Для чтения поста из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime