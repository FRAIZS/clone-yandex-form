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