from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.db.database import get_db
from app.schemas.auth import Signup, TokenResponse
from app.models.models import User
from app.utils.responses import ResponseHandler


class AuthService:
    @staticmethod
    async def signup(user: Signup, db: Session):
        # Hash the password of the user.
        user.password = hash_password(user.password)

        # Generate the object of the user.
        db_user = User(**user.model_dump())

        # The add the user to the database.
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        # First get the user having the username in the submitted credentials
        user = db.query(User).filter(User.username == user_credentials.username).first()

        # If the user is null
        if not user:
            raise ResponseHandler.auth_bad_request_error()

        # Verification of the user's password.
        if not verify_password(user_credentials.password, user.password):
            raise ResponseHandler.auth_bad_request_error()

        # Return the token.
        access_token = await create_access_token(data={"sub": user.username}, expire_delta=timedelta(minutes=settings.access_token_expire_minutes))
        return TokenResponse(access_token=access_token, expires_in=settings.access_token_expire_minutes)





