from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr

from app.schemas.auth import BaseConfig

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str
    is_active: bool
    created_at: datetime

    class Config(BaseConfig):
        pass


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

    class Config(BaseConfig):
        pass


class UserUpdate(UserCreate):
    pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


class UsersOut(BaseModel):
    message: str
    data: List[UserBase]

    class Config(BaseConfig):
        pass


class UserOutDelete(BaseConfig):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass
