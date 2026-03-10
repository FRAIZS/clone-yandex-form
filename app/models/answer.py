from sqlalchemy import Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime

class FormResponse(Base):
    __tablename__ = "form_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Связи
    form = relationship("Form")
    user = relationship("User")
    answers = relationship("Answer", back_populates="response", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("form_responses.id", ondelete="CASCADE"))
    field_id: Mapped[int] = mapped_column(ForeignKey("fields.id", ondelete="CASCADE"))
    
    # сохнарить ответ как JSON, в чекбоксах это может быть список строк
    value: Mapped[dict] = mapped_column(JSON, nullable=False)

    response = relationship("FormResponse", back_populates="answers")
    field = relationship("Field")