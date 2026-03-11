from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from ..schemas.user import User
from ..schemas.category import Category
from ..schemas.location import Location


class PostBase(BaseModel):
    """Базовая модель поста"""
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    author_id: int
    category_id: int | None = None
    location_id: int | None = None
    image: str | None = None
    is_published: bool = True


class PostCreate(PostBase):
    """Для создания поста"""
    pass


class PostUpdate(BaseModel):
    """Для обновления поста - все поля необязательные"""
    title: str | None = Field(None, max_length=256)
    text: str | None = None
    pub_date: datetime | None = None
    author_id: int | None = None
    category_id: int | None = None
    location_id: int | None = None
    image: str | None = None
    is_published: bool | None = None


class Post(PostBase):
    """Для чтения поста из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    # Можно добавить расширенные поля с данными связанных объектов
    author: User | None = None
    category: Category | None = None
    location: Location | None = None


class PostDetail(Post):
    """Детальная информация о посте со всеми связями"""
    pass