import time
from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

class QuestionRequest(BaseModel):
    prompt: str

@router.post("/ask-typhoon-summary")
def ask_typhoon_summary(request: QuestionRequest):
    start_time = time.time()

    llm = Typhoon2Assistant(system_content="ช่วยสรุปข้อความที่รับมาให้เข้าใจง่าย สั้นกระชับ และไม่ยาวมากนัก ใน 1 paragraph")
    answer = llm.ask(request.prompt)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return {
        "answer": answer,
        "prompt": request.prompt,
        "execution_time": execution_time
    }
