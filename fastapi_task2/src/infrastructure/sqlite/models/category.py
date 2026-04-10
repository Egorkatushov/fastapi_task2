# src/infrastructure/sqlite/models/category.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)  # ← должно быть title, а не name
    description = Column(Text, nullable=False)
    slug = Column(String(64), nullable=False, unique=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())