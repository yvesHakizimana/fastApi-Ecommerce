from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr

from app.schemas.carts import CartBase


class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str
    is_active: bool
    created_at: datetime
    carts: List[CartBase]

    class Config(BaseConfig):
        pass


class Signup(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str

    class Config(BaseConfig):
        pass


class UserBaseOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config(BaseConfig):
        pass


class UserOut(BaseModel):
    message: str
    data: UserBaseOut

    class Config(BaseConfig):
        pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    expires_in: int
