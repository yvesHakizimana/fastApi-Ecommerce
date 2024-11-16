from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.categories import CategoriesOut, CategoryOut, CategoryCreate, CategoryUpdate
from app.services.categories import CategoryService

router = APIRouter(tags=["categories"], prefix="/categories")


@router.get("/", response_model=CategoriesOut)
def get_all_categories(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page Number"),
        limit: int = Query(10, ge=1, description="Items per page"),
        search: str | None = Query("", description="Search based on the name of categories"),
):
    return CategoryService.get_all_categories(db, page, limit, search)


@router.get("/{category_id}", response_model=CategoryOut)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.get_category(db, category_id)


@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryService.create_category(db, category)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_update: CategoryUpdate,  category_id: int, db: Session = Depends(get_db)):
    return CategoryService.update_category(db, category_id, category_update)


@router.delete("/{category_id}", response_model=CategoryOut)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService.delete_category(db, category_id)




