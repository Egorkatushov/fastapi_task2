from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    text: str
    post_id: int
    author_id: int


class CommentCreate(CommentBase):
    id: int
    created_at: datetime


class CommentUpdate(BaseModel):
    text: Optional[str] = None


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime