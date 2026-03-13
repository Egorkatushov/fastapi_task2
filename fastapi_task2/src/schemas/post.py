from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from ..schemas.user import User
from ..schemas.category import Category
from ..schemas.location import Location


class PostBase(BaseModel):
    """Базовая модель поста"""
    title: str = Field(..., max_length=256, description="Заголовок поста")
    text: str = Field(..., description="Текст поста")
    pub_date: datetime = Field(..., description="Дата публикации")
    author_id: int = Field(..., description="ID автора")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, description="URL изображения")
    is_published: bool = Field(True, description="Опубликован ли пост")


class PostCreate(PostBase):
    """Для создания поста"""
    pass


class PostUpdate(BaseModel):
    """Для обновления поста - все поля необязательные"""
    title: Optional[str] = Field(None, max_length=256, description="Заголовок поста")
    text: Optional[str] = Field(None, description="Текст поста")
    pub_date: Optional[datetime] = Field(None, description="Дата публикации")
    author_id: Optional[int] = Field(None, description="ID автора")
    category_id: Optional[int] = Field(None, description="ID категории")
    location_id: Optional[int] = Field(None, description="ID локации")
    image: Optional[str] = Field(None, description="URL изображения")
    is_published: Optional[bool] = Field(None, description="Опубликован ли пост")


class Post(PostBase):
    """Для чтения поста из БД (базовая информация)"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class PostWithRelations(Post):
    """Пост с расширенной информацией о связанных объектах"""
    author: Optional[User] = None
    category: Optional[Category] = None
    location: Optional[Location] = None


class PostDetail(PostWithRelations):
    """Детальная информация о посте со всеми связями"""
    # Можно добавить комментарии к посту, если нужно
    # comments: List[Comment] = []
    pass