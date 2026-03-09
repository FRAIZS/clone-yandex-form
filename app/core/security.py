import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from app.core.config import settings

def get_hash_pwd(pwd: str) -> str:
    """Превращает пароль в защищенный хеш"""
    # Превращаем пароль в байты
    pwd_bytes = pwd.encode('utf-8')
    # Генерируем "соль"
    salt = bcrypt.gensalt()
    # Хешируем
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Возвращаем как строку для базы данных
    return hashed.decode('utf-8')

def verify_password(plain_pwd: str, hash_pwd: str) -> bool:
    """Проверяет, совпадает ли введенный пароль с хешем из базы"""
    password_bytes = plain_pwd.encode('utf-8')
    hashed_bytes = hash_pwd.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен (код остается прежним)"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt