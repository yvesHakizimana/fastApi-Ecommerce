from sqlalchemy.orm import Session

from app.core.security import get_username_from_token, verify_password
from app.models.models import User
from app.schemas.accounts import AccountUpdate
from app.utils.responses import ResponseHandler


class AccountService:
    @staticmethod
    async def get_my_info(db: Session, token):
        # Get the username from returned payload
        active_user_username = await get_username_from_token(token)

        # Validate if the username is within in the database
        db_user = db.query(User).filter(User.username == active_user_username).first()
        if not db_user:
            return ResponseHandler.not_found_error("User", active_user_username)

        # Return the profile of logged-in user
        return ResponseHandler.get_single_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def edit_my_info(db: Session, token, updated_user: AccountUpdate):
        active_user_username = await get_username_from_token(token)
        db_user = db.query(User).filter(User.username == active_user_username).first()
        if not db_user:
            return ResponseHandler.not_found_error("User", active_user_username)

        # update the user with the information from fronted/api.
        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.update_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def remove_my_account(db: Session, token):
        active_user_username = await get_username_from_token(token)
        db_user = db.query(User).filter(User.username == active_user_username).first()
        if not db_user:
            return ResponseHandler.not_found_error("User", active_user_username)
        db.delete(db_user)
        db.commit()
        return ResponseHandler.delete_success(db_user.username, db_user.id, db_user)



