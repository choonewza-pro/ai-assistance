from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask-typhoon-summary")
def ask_typhoon_summary(request: QuestionRequest):
    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ช่วยสรุปข้อความที่รับมาให้เข้าใจง่ายและไม่ยาวมากนัก")
    answer = llm.ask(request.question)
    return {
        "success": True,
        "result": {
            "answer": answer,
        },
        "input": {
            "question": request.question,
        }
    }
