from datetime import datetime
from typing import List, ClassVar

from pydantic import BaseModel, field_validator

from app.schemas.categories import CategoryBase


class BaseConfig:
    from_attributes = True


class ProductBase(BaseModel):
    id: int
    title: str
    description: str
    price: int

    @field_validator("discount_percentage")
    def validate_discount_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        return v
    discount_percentage: float
    rating: float
    stock: int
    brand: str
    thumbnail: str
    images: List[str]
    is_published: bool
    created_at: datetime
    category_id: int
    category: CategoryBase

    class Config(BaseConfig):
        pass


class ProductCreate(ProductBase):
    id: ClassVar[int]
    category: ClassVar[CategoryBase]

    class Config(BaseConfig):
        pass


class ProductUpdate(ProductCreate):
    pass


class ProductOut(BaseModel):
    message: str
    data: ProductBase

    class Config(BaseConfig):
        pass


class ProductsOut(BaseModel):
    message: str
    data: List[ProductBase]

    class config(BaseConfig):
        pass


class ProductDelete(ProductBase):
    category: ClassVar[CategoryBase]


class ProductOutDelete(BaseModel):
    message: str
    data: ProductDelete



