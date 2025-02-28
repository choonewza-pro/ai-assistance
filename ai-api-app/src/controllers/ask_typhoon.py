import time
from fastapi import APIRouter, Query
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

@router.get("/ask-typhoon")
def ask_typhoon(
    prompt: str = Query(..., description="The prompt to ask the website"),
):
    start_time = time.time()

    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี")
    answer = llm.ask(prompt)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "answer": answer,
        "prompt": prompt,
        "execution_time": execution_time
    }
