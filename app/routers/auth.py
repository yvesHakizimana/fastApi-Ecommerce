from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import auth
from app.schemas.auth import Signup
from app.services.auth import AuthService

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=auth.UserOut)
async def signup(user: Signup, db: Session = Depends(get_db)):
    return await AuthService.signup(user=user, db=db)


@router.post("/token", status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await AuthService.login(user_credentials=user_credentials, db=db)
