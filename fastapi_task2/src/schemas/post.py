from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from src.schemas.user import User
from src.schemas.category import Category
from src.schemas.location import Location


class PostBase(BaseModel):
    title: str = Field(max_length=256)
    text: str
    pub_date: datetime
    author_id: int
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    image: Optional[str] = None
    is_published: bool = True


class PostCreate(PostBase):
    id: int
    created_at: datetime


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    location_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class PostWithRelations(Post):
    author: Optional[User] = None
    category: Optional[Category] = None
    location: Optional[Location] = None


class PostDetail(PostWithRelations):
    pass