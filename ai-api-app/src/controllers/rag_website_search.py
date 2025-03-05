import time
import os
from fastapi import APIRouter, Query
from src.utils.ask_websites import AskWebs

router = APIRouter()

@router.get("/rag-website-search")
def rag_website_search(
    question: str = Query(..., description="The URL of the website to query"),
):
    start_time = time.time()

    askWebs = AskWebs()
    result = askWebs.search_website_chunks(question=question);
    
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time1": execution_time,
        "vector_store_details": result["vector_store_details"],
        "retrieved_docs": result["retrieved_docs"],
    }