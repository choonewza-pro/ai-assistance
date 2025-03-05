import time
from fastapi import APIRouter, Query
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

@router.get("/ask-typhoon")
def ask_typhoon(
    prompt: str = Query(..., description="The prompt to ask the website"),
    model: str = Query("1b", description="The model ID to use 1b or 3b")
):
    start_time = time.time()
    
    model_id = "scb10x/llama3.2-typhoon2-1b-instruct"
    if model == "3b":
        model_id ="scb10x/llama3.2-typhoon2-3b-instruct"

    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี",model_id=model_id)
    answer = llm.ask(prompt)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "answer": answer,
        "prompt": prompt,
        "execution_time": execution_time,
        "model": model_id
    }
