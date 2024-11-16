from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.product import ProductsOut, ProductOut, ProductCreate, ProductUpdate
from app.services.products import ProductService

router = APIRouter(tags=["products"], prefix="/products")


# Get all products
@router.get('/', response_model=ProductsOut)
def get_all_products(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(5, ge=1, description="Products per page"),
        search: str | None = Query("", description="Search based on the title of the product"),
):
    return ProductService.get_all_products(db, page, limit, search)


# Get a single product.
@router.get('/{product_id}', response_model=ProductOut)
def get_single_product(
        product_id: int,
        db: Session = Depends(get_db),
):
    return ProductService.get_product_by_id(db, product_id)


# Create a product
@router.post('/', response_model=ProductOut)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db),
):
    return ProductService.create_product(db, product)


# update the properties of a product.
@router.put('/{product_id}', response_model=ProductOut)
def update_product(
        product_id: int,
        product: ProductUpdate,
        db: Session = Depends(get_db),
):
    return ProductService.update_product(db, product_id, product)


# Delete a product
@router.delete('/{product_id}', response_model=ProductOut)
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
):
    return ProductService.delete_product(db, product_id)


