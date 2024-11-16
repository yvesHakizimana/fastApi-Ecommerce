from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme
from app.db.database import get_db
from app.schemas.accounts import AccountOut, AccountUpdate
from app.services.account import AccountService

router = APIRouter(tags=["Account"], prefix="/account")


@router.get('/me', response_model=AccountOut)
async def get_my_info(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return await AccountService.get_my_info(db, token)


@router.put('/me', response_model=AccountOut)
async def edit_my_info(token: Annotated[str, Depends(oauth2_scheme)], updated_user: AccountUpdate, db: Session = Depends(get_db)):
    return await AccountService.edit_my_info(db, updated_user, token)


@router.delete('/me', response_model=AccountOut)
async def remove_account(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return await AccountService.remove_my_account(db, token)



