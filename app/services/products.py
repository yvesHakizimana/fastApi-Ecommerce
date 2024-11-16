from sqlalchemy.orm import Session

from app.models.models import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.responses import ResponseHandler


class ProductService:
    @staticmethod
    def get_all_products(
            db: Session,
            page: int,
            limit: int,
            search: str = "",
    ):
        products = (db.query(Product)
                    .order_by(Product.id.asc())
                    .filter(Product.title.contains(search))
                    .offset((page - 1) * limit)
                    .limit(limit).all())
        return {"message": f"page {page} with {limit} products", "data": products}

    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            ResponseHandler.not_found_error("Product",product_id)
        return ResponseHandler.get_single_success(product.title, product_id, product)

    @staticmethod
    def create_product(db: Session, product: ProductCreate):
        # First find if the category exists
        category_exists = db.query(Category).filter(Category.id == product.category_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("Category",product.category_id)

        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def update_product(
            db: Session,
            product_id: int,
            product: ProductUpdate,
    ):
        # First find the existing product
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product",product_id)
        # Update the corresponding object accordingly.
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return ResponseHandler.update_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            ResponseHandler.not_found_error("Product",product_id)
        db.delete(db_product)
        db.commit()
        return ResponseHandler.delete_success(db_product.title, db_product.id, db_product)
