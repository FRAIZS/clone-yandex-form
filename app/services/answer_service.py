from sqlalchemy.orm import Session
from app.models.answer import FormResponse, Answer
from app.schemas.answer import ResponseCreate

def create_response(db: Session, form_id: int, user_id: int, response_data: ResponseCreate):
    # Создаем запись о заполнения анкеты
    db_response = FormResponse(form_id=form_id, user_id=user_id)
    db.add(db_response)
    db.flush() # Получаем ID ответа

    # Сохраняем ответ на вопрос
    for answer_data in response_data.answers:
        db_answer = Answer(
            response_id=db_response.id,
            field_id=answer_data.field_id,
            value=answer_data.value 
        )
        db.add(db_answer)
    
    db.commit()
    db.refresh(db_response)
    return db_response

# Получаем все ответы на форму 
def get_responses_by_form(db: Session, form_id: int):
    return db.query(FormResponse).filter(FormResponse.form_id == form_id).all()