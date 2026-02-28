from datetime import datetime, timedelta, timezone

from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Насторойка контекста хэширования пароля 
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto') # pwd - password

# Проверка совпадает ли пароль с хэшем 
def verify_password(plain_pwd: str, hash_pwd: str) -> bool:
    return pwd_context.verify(plain_pwd, hash_pwd)

# Переводит пароль в хэш
def get_hash_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)

#Создание JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) 
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt