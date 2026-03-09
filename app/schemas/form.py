from pydantic import BaseModel
from typing import List, Optional

# Схема для одного поля 
class FieldBase(BaseModel):
    type: str 
    label: str
    options: Optional[List[str]] = None 

# Схема для создания формы с вложенными полями
class FormCreate(BaseModel):
    title: str
    description: Optional[str] = None
    fields: List[FieldBase]

# Схема для отображения поля с ID
class FieldResponse(FieldBase):
    id: int
    class Config:
        from_attributes = True

# Схема для отображения формы с ID и списком полей
class FormResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner_id: int
    fields: List[FieldResponse]

    class Config:
        from_attributes = True