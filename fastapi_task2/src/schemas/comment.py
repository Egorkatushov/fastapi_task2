from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    """Базовая модель комментария"""
    text: str = Field(min_length=1, description="Текст комментария")
    post_id: int = Field(description="ID поста, к которому относится комментарий")
    author_id: int = Field(description="ID автора комментария")


class CommentCreate(CommentBase):
    """Для создания комментария"""
    pass


class CommentUpdate(BaseModel):
    """Для обновления комментария - только текст можно менять"""
    text: str = Field(min_length=1, description="Новый текст комментария")


class Comment(CommentBase):
    """Для чтения комментария из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime