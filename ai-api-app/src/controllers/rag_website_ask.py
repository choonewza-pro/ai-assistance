import time
import os
from fastapi import APIRouter, Query
from src.utils.typhoon_2_assistant import Typhoon2Assistant
from src.utils.ask_websites import AskWebs

router = APIRouter()

@router.get("/rag-website-ask")
def rag_website_ask(
    question: str = Query(..., description="The URL of the website to query"),
    model: str = Query("1b", description="The model ID to use 1b or 3b")
):
    start_time = time.time()

    model_id = "scb10x/llama3.2-typhoon2-1b-instruct"

    if model == "3b":
        model_id ="scb10x/llama3.2-typhoon2-3b-instruct"

    askWebs = AskWebs()
    result = askWebs.genPrompt(question=question);

    llm = Typhoon2Assistant(system_content=result["system_role"],model_id=model_id)
    answer = llm.ask(result["prompt"])
    
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "answer": answer,
        "model": model_id,
        "prompt": result["prompt"],
        "question": question,
        "retrieved_docs": result["retrieved_docs"],
        "vector_store_details": result["vector_store_details"],
    }