from sqlalchemy import String, Text, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..database import Base


class Post(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    text: Mapped[str] = mapped_column(Text)
    pub_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    image: Mapped[str] = mapped_column(String(100), nullable=True)

    # Foreign Keys
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_user.id"))
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_location.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_category.id"), nullable=True)

    # Relationships
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    location = relationship("Location", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"