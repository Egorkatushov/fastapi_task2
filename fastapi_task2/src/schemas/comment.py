from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    """Базовая модель комментария"""
    text: str
    post_id: int
    author_id: int


class CommentCreate(CommentBase):
    """Для создания комментария"""
    pass


class CommentUpdate(BaseModel):
    """Для обновления комментария"""
    text: str | None = None


class Comment(CommentBase):
    """Для чтения комментария из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime