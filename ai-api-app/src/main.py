from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.controllers.ask_website import router as ask_website_router
from src.controllers.ask_pdf import router as ask_pdf_router
from src.controllers.ask_typhoon import router as ask_typhoon_router
from src.controllers.ask_typhoon_summary import router as ask_typhoon_summary_router
from src.controllers.rag_pdf_load import router as rag_pdf_load
from src.controllers.rag_pdf_search import router as rag_pdf_search
from src.controllers.rag_pdf_ask import router as rag_pdf_ask

app = FastAPI()
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/ping")
def hello():
    return {"response": "pong"}

app.include_router(ask_website_router)
app.include_router(ask_pdf_router)
app.include_router(ask_typhoon_router)
app.include_router(ask_typhoon_summary_router)
app.include_router(rag_pdf_load)
app.include_router(rag_pdf_search)
app.include_router(rag_pdf_ask)