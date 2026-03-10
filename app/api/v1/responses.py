from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api import deps
from app.schemas.answer import ResponseCreate, FormResponseOut
from app.services import answer_service, form_service
from app.models.user import User

router = APIRouter(prefix="/forms", tags=["responses"])

@router.post("/{form_id}/answers", response_model=FormResponseOut)
def submit_form_answers(
    form_id: int,
    response_data: ResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Проверяем, существует ли форма
    db_form = form_service.get_form_by_id(db, form_id)
    if not db_form:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    
    # Можно добавить проверку: принадлежат ли присланные field_id этой форме
    form_field_ids = [f.id for f in db_form.fields]
    for ans in response_data.answers:
        if ans.field_id not in form_field_ids:
            raise HTTPException(
                status_code=400, 
                detail=f"Поле с ID {ans.field_id} не принадлежит этой форме"
            )

    return answer_service.create_response(
        db=db, 
        form_id=form_id, 
        user_id=current_user.id, 
        response_data=response_data
    )