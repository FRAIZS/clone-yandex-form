from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

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