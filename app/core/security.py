from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.db.database import get_db
from app.models.models import User

# Password context for handling password hashing and verification mechanims
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Create Hash Password
def hash_password(password) -> str:
    return pwd_context.hash(password)


# Verify Hash Password
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Creation of access token
async def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def get_username_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username


# Check Admin Role
async def check_admin_role(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    active_user_username = await get_username_from_token(token)
    db_active_user = db.query(User).filter(User.username == active_user_username).first()
    if db_active_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin role is required.")

