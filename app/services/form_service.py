from app.models.form import Form, Field
from app.schemas.form import FormCreate

from sqlalchemy.orm import Session

def create_form(db: Session, form_schema: FormCreate, owner_id: int):
    # Созжание формы
    new_form = Form(
        title=form_schema.title,
        description=form_schema.description,
        owner_id=owner_id
    )
    
    db.add(new_form)
    db.flush()
    
    for field_data in form_schema.fields:
        new_fields = Field(
            form_id=new_form.id,
            type=field_data.type,
            label=field_data.label,
            options=field_data.options #Это JSON
        )
        db.add(new_fields)
        
    db.commit()
    db.refresh(new_form)
    return new_form

def get_form_by_id(db: Session, form_id: int):
    return db.query(Form).filter(Form.id == form_id).first()

def delete_form(db: Session, form_id: int):
    form = get_form_by_id(db, form_id)
    if form:
        db.delete(form)
        db.commit()
    return form

def update_form(db: Session, form_id: int, form_data: FormCreate):
    db_form = get_form_by_id(db, form_id)
    if not db_form:
        return None
    
    # Обновляем основные поля формы
    db_form.title = form_data.title
    db_form.description = form_data.description
    
    # Обновление полей - проще всего удалить старые и создать новые
    # Удаляем старые поля
    for old_field in db_form.fields:
        db.delete(old_field)
    
    # Добавляем новые из запроса
    for field_data in form_data.fields:
        new_field = Field(
            form_id=db_form.id,
            type=field_data.type,
            label=field_data.label,
            options=field_data.options
        )
        db.add(new_field)

    db.commit()
    db.refresh(db_form)
    return db_form