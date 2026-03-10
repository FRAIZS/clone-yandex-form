from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.api import deps
from app.schemas.form import FormCreate, FormResponse
from app.services import form_service
from app.models.user import User

router = APIRouter(prefix="/forms", tags=["forms"])

@router.post("/", response_model=FormResponse)
def create_new_form(
    form_data: FormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user) 
):
    """Создать новую форму с полями"""
    return form_service.create_form(db=db, form_schema=form_data, owner_id=current_user.id)

@router.get("/{form_id}", response_model=FormResponse)
def get_form(form_id: int, db: Session = Depends(get_db)):
    db_form = form_service.get_form_by_id(db, form_id)
    if not db_form:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    return db_form

@router.delete("/{form_id}")
def delete_form(
    form_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(deps.get_current_user)
):
    db_form = form_service.get_form_by_id(db, form_id)
    if not db_form:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    
    # Проверка: является ли пользователь владельцем?
    if db_form.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    form_service.delete_form(db, form_id)
    return {"message": "Форма успешно удалена"}

@router.put("/{form_id}", response_model=FormResponse)
def update_form(
    form_id: int,
    form_data: FormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_form = form_service.get_form_by_id(db, form_id)
    if not db_form:
        raise HTTPException(status_code=404, detail="Форма не найдена")
    
    if db_form.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
        
    return form_service.update_form(db, form_id, form_data)

@router.get("/", response_model=List[FormResponse])
def get_my_forms(
    search: Optional[str] = None,
    sort_by: Optional[str] = "id",
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return form_service.get_user_forms(
        db=db,
        owner_id=current_user.id,
        search=search,
        sort_by=sort_by,
    )