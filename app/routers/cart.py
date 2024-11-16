from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.security import oauth2_scheme
from app.db.database import get_db
from app.schemas.carts import CartsOutList, CartUpdate, CartCreate, CartOut, CartOutDelete
from app.services.cart import CartService

router = APIRouter(tags=["Cart"], prefix="/cart")


# Get All Carts
@router.get("/", status_code=status.HTTP_200_OK, response_model=CartsOutList)
def get_all_carts(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
):
    return CartService.get_all_carts(token, db, page, limit)


# Get Cart By Cart ID
@router.get("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def get_cart(
        cart_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
):
    return await CartService.get_cart(token, db, cart_id)


# Create New Cart
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CartOut)
async def create_cart(
        cart: CartCreate,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
):
    return await CartService.create_cart(token, db, cart)


# Update Existing Cart
@router.put("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOut)
async def update_cart(
        cart_id: int,
        updated_cart: CartUpdate,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
):
    return await CartService.update_cart(token, db, cart_id, updated_cart)


# Delete Cart By Cart ID
@router.delete("/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartOutDelete)
async def delete_cart(
        cart_id: int,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
):
    return await CartService.delete_cart(token, db, cart_id)

