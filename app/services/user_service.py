from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import CreateUser
from app.core.security import get_hash_pwd, verify_password

# Получить пользователя по имени 
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_schema: CreateUser):
    hashed_pwd = get_hash_pwd(user_schema.password)
    new_user = User(username=user_schema.username, hashed_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def auth_user(db: Session, username: str, pwd: str):
    user = get_user_by_username(db, username)
    if not user:
        return "Пользователь с данным именем не найден"
    if not verify_password(pwd, user.hashed_password):
        return "Не верный пароль"
    return user
    