from fastapi import FastAPI
from src.controllers.reg_website import router as reg_website_router

app = FastAPI()

@app.get("/ping")
def hello():
    return {"response": "pong"}

app.include_router(reg_website_router)