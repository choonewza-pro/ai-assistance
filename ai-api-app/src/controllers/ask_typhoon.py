from fastapi import APIRouter, Query
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

@router.get("/ask-typhoon")
def ask_typhoon(
    prompt: str = Query(..., description="The prompt to ask the website"),
):
    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี")
    answer = llm.ask(prompt)
    return {
        "success": True,
        "result":{
            "answer": answer,
        },
        "input":{
            "prompt": prompt,
        }
    }
