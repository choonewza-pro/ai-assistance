import time
from fastapi import APIRouter
from src.utils.ask_websites import AskWebs

router = APIRouter()

@router.get("/rag-website-reset")
def rag_website_reset():
    start_time = time.time()

    askWebs = AskWebs()
    askWebs.resetAllDocuments();
    
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time1": execution_time,
        "reset_all_documents": True
    }