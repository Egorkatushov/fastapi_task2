from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    first_name: str = Field(default="", max_length=150)
    last_name: str = Field(default="", max_length=150)


class UserCreate(UserBase):
    id: int
    password: str = Field(min_length=6)
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    date_joined: datetime
    last_login: Optional[datetime] = None


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    first_name: Optional[str] = Field(None, max_length=150)
    last_name: Optional[str] = Field(None, max_length=150)
    is_active: Optional[bool] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    is_staff: bool
    last_login: Optional[datetime] = None
    date_joined: datetime