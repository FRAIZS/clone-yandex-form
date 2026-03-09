from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import CreateUser, ResponseUser, Token
from app.services import user_service
from app.core.security import create_access_token
from app.core.config import settings
from app.api import deps
from app.models.user import User

from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=ResponseUser)
def register(user_data: CreateUser, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_username(db, user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")
    return user_service.create_user(db=db, user_schema=user_data)

@router.post("/login", response_model=Token)
def login(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.auth_user(db=db, username=from_data.username, pwd=from_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не правильный пароль")
    
    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expire
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=ResponseUser)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    return current_user # Информация о текущем токене пользователя 