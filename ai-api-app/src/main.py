from fastapi import FastAPI
from src.controllers.ask_website import router as ask_website_router
from src.controllers.ask_pdf import router as ask_pdf_router

app = FastAPI()

@app.get("/ping")
def hello():
    return {"response": "pong"}

app.include_router(ask_website_router)
app.include_router(ask_pdf_router)