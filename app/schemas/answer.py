from pydantic import BaseModel
from typing import List, Any, Optional
from datetime import datetime

# Одиночный ответ на вопрос
class AnswerCreate(BaseModel):
    field_id: int
    value: Any 
    
# Группа ответов - вся анкета
class ResponseCreate(BaseModel):
    answers: List[AnswerCreate]

# Для отображения ответа 
class AnswerResponse(BaseModel):
    field_id: int
    value: Any
    class Config:
        from_attributes = True

class FormResponseOut(BaseModel):
    id: int
    form_id: int
    user_id: int
    created_at: datetime
    answers: List[AnswerResponse]
    class Config:
        from_attributes = True