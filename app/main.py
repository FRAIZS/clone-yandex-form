from fastapi import FastAPI

from app.db.session import engine, Base
from app.models import user

#Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API клон яндекс формы"
)

@app.get("/")
def root():
    return {"message" : "hello world, table created"}