from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.controllers.ask_typhoon import router as ask_typhoon_router
from src.controllers.ask_typhoon_summary import router as ask_typhoon_summary_router
from src.controllers.ask_typhoon_stream import router as ask_typhoon_stream_router


from src.controllers.rag_pdf_list_pdfs import router as rag_pdf_list_pdfs

from src.controllers.rag_pdf_load import router as rag_pdf_load
from src.controllers.rag_pdf_search import router as rag_pdf_search
from src.controllers.rag_pdf_prompt import router as rag_pdf_prompt
from src.controllers.rag_pdf_ask import router as rag_pdf_ask


from src.controllers.rag_website_load import router as rag_website_load
from src.controllers.rag_website_reset import router as rag_website_reset
from src.controllers.rag_website_search import router as rag_website_search
from src.controllers.rag_website_prompt import router as rag_website_prompt
from src.controllers.rag_website_ask import router as rag_website_ask

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/ping")
def hello():
    return {"response": "pong"}

app.include_router(ask_typhoon_router)
app.include_router(ask_typhoon_summary_router)
app.include_router(ask_typhoon_stream_router)
app.include_router(rag_pdf_list_pdfs)
app.include_router(rag_pdf_load)
app.include_router(rag_pdf_search)
app.include_router(rag_pdf_prompt)
app.include_router(rag_pdf_ask)
app.include_router(rag_website_load)
app.include_router(rag_website_reset)
app.include_router(rag_website_search)
app.include_router(rag_website_prompt)
app.include_router(rag_website_ask)