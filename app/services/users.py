from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.models import User
from app.schemas.users import UserCreate, UserUpdate
from app.utils.responses import ResponseHandler


class UsersService:
    # Getting users through pagination: page, limit  and searchString
    @staticmethod
    def get_all_users(db: Session, page: int, limit: int, search: str = "", role: str = 'user'):
        users = db.query(User).order_by(User.id.asc()).filter(User.username.contains(search), User.role == role).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"page {page} with {limit} users", "data": users}

    @staticmethod
    def get_user(db: Session, user_id):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            ResponseHandler.not_found_error("User", user_id)
        return ResponseHandler.get_single_success(user.username, user_id, user)

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        user.password = hash_password(user.password)
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return ResponseHandler.create_success(new_user.username, new_user.id, new_user)

    @staticmethod
    def update_user(db: Session, user_id: int, updated_user: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return ResponseHandler.update_success(db_user.username, db_user.id, db_user)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)
        db.delete(db_user)
        db.commit()
        return ResponseHandler.delete_success(db_user.username, db_user.id, db_user)




