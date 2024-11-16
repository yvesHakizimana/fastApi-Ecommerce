from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.schemas.product import ProductBase, CategoryBase


# Base Config
class BaseConfig:
    from_attributes = True


class ProductBaseCart(ProductBase):
    category: CategoryBase = Field(exclude=True)

    class Config(BaseConfig):
        pass


# Base Cart & Cart_Item
class CartItemBase(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product: ProductBaseCart


# The whole cart containing the cart items.
class CartBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    cart_items: List[CartItemBase]

    class Config(BaseConfig):
        pass


# The same as cart base , containing the user created cart and also cart_items
class CartOutBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    cart_items: List[CartItemBase]

    class Config(BaseConfig):
        pass


# Get Cart to mean the cart the whole cart of the user containing also the cart items
class CartOut(BaseModel):
    message: str
    data: CartBase

    class Config(BaseConfig):
        pass


# The list of all carts in the system
class CartsOutList(BaseModel):
    message: str
    data: List[CartBase]


# The cart corresponding to the logged-in user.
class CartsUserOutList(BaseModel):
    message: str
    data: List[CartBase]

    class Config(BaseConfig):
        pass


# Delete Cart of cartItems.
class CartOutDelete(BaseModel):
    message: str
    data: CartOutBase


# Create Cart
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartCreate(BaseModel):
    cart_items: List[CartItemCreate]

    class Config(BaseConfig):
        pass


# Update Cart
class CartUpdate(CartCreate):
    pass
