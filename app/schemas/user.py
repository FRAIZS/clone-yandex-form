from pydantic import BaseModel
from typing import Optional

# Что ждем от пользователя 
class CreateUser(BaseModel):
    username: str
    password: str

# Что отдаем пользователю 
class ResponseUser(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    username: Optional[str] = None