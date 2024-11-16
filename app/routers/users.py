from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import check_admin_role
from app.db.database import get_db
from app.schemas.auth import UserOut
from app.schemas.users import UserCreate, UserUpdate, UsersOut
from app.services.users import UsersService

router = APIRouter(tags=["users"], prefix="/users")


# This is route is only for admin so it before getting the data it must check if the logged_in user is admin.
@router.get("/", response_model=UsersOut, dependencies=[Depends(check_admin_role)], status_code=status.HTTP_200_OK)
def get_all_users(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(1, ge=1, le=100,  description="Items per page"),
        search: str | None = Query("", description="Search based username"),
        role: str = Query("user", enum=["user", "admin"], description="Role"),
):
    return UsersService.get_all_users(db, page, limit, search, role)


@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(check_admin_role)], status_code=status.HTTP_200_OK)
def get_all(user_id: int, db: Session = Depends(get_db)):
    return UsersService.get_user(db, user_id)


@router.post("/", response_model=UserOut, dependencies=[Depends(check_admin_role)], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UsersService.create_user(db, user)


@router.put("/{user_id}", response_model=UserOut, dependencies=[Depends(check_admin_role)],  status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UsersService.update_user(db=db, user_id=user_id, updated_user=user)


@router.delete("/{user_id}", response_model=UserOut, dependencies=[Depends(check_admin_role)], status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UsersService.delete_user(db=db, user_id=user_id)


