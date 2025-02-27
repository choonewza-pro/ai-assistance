from fastapi import APIRouter, Query
from src.utils.ask_pdf import AskPDF
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

@router.get("/ask-typhoon")
def ask_typhoon(
    question: str = Query(..., description="The question to ask the website"),
):
    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี")
    answer = llm.ask(question)
    return {
        "success": True,
        "result":{
            "answer": answer,
        },
        "input":{
            "question": question,
        }
    }
