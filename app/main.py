from fastapi import FastAPI

app = FastAPI(
    title="API клон яндекс формы"
)

@app.get("/")
def root():
    return {"message" : "hello world"}