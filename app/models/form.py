from sqlalchemy import Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from typing import List, Optional

class Form(Base):
    __tablename__ = "forms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Связь с пользователем
    owner = relationship("User", back_populates="forms")
    # Связь с полями (вопросами)
    fields = relationship("Field", back_populates="form", cascade="all, delete-orphan")

class Field(Base):
    __tablename__ = "fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"))
    
    # Тип поля text, radio, checkbox
    type: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    
    # Варианты ответа (только для radio и checkbox). Храним как список ["Да", "Нет"]
    options: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    form = relationship("Form", back_populates="fields")