from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

class QuestionRequest(BaseModel):
    prompt: str

@router.post("/ask-typhoon-summary")
def ask_typhoon_summary(request: QuestionRequest):
    llm = Typhoon2Assistant(system_content="ช่วยสรุปข้อความที่รับมาให้เข้าใจง่าย สั้นกระชับ และไม่ยาวมากนัก ใน 1 paragraph")
    answer = llm.ask(request.prompt)
    return {
        "success": True,
        "result": {
            "answer": answer,
        },
        "input": {
            "prompt": request.prompt,
        }
    }
