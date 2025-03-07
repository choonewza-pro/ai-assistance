import time
import os
from fastapi import APIRouter, Query
from src.utils.ask_websites import AskWebs
from src.utils.fix_thai_text import fix_thai_text

router = APIRouter()

@router.get("/rag-website-prompt")
def rag_website_prompt(
    question: str = Query(..., description="The URL of the website to query"),
):
    start_time = time.time()

    askWebs = AskWebs()
    result = askWebs.genPrompt(question=question);

    prompt_fix = fix_thai_text(result["prompt"])
    
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "prompt": prompt_fix,
        "question": question,
        "retrieved_docs": result["retrieved_docs"],
        "vector_store_details": result["vector_store_details"],
    }