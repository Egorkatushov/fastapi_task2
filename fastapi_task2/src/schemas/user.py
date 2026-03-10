from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Базовая модель пользователя"""
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    first_name: str = Field(min_length=3, max_length=64)
    last_name: str = Field(min_length=3, max_length=64)


class UserCreate(UserBase):
    """Для создания пользователя"""
    password: str = Field(min_length=6)


class UserUpdate(BaseModel):
    """Для обновления пользователя"""
    username: str | None = Field(None, min_length=3, max_length=64)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)
    first_name: str | None = Field(None, min_length=3, max_length=64)
    last_name: str | None = Field(None, min_length=3, max_length=64)


class User(UserBase):
    """Для чтения пользователя из БД"""
    model_config = ConfigDict(from_attributes=True)

    id: int