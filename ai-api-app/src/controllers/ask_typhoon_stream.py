from fastapi import APIRouter, Query
from src.utils.typhoon_2_assistant import Typhoon2Assistant
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/ask-typhoon-stream")
# def ask_typhoon_stream(
#     prompt: str = Query(..., description="The prompt to ask the website"),
#     model: str = Query("1b", description="The model ID to use 1b or 3b")
# ):    
#     model_id = "scb10x/llama3.2-typhoon2-1b-instruct"
#     if model == "3b":
#         model_id ="scb10x/llama3.2-typhoon2-3b-instruct"

#     llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี",model_id=model_id)
    
#     def generate():
#         for answer in llm.ask_stream(prompt):
#             print(answer)
#             yield answer + "\n"

#     return StreamingResponse(generate(), media_type="text/plain")


# curl -G "http://localhost/ask-typhoon-stream" --data-urlencode "prompt=ไก่กับไข่อะไรเกิดก่อนกัน?" --data-urlencode "model=1b"


def ask_typhoon_stream(
    prompt: str = Query(..., description="The prompt to ask the website"),
    model: str = Query("1b", description="The model ID to use 1b or 3b")
):    
    model_id = "scb10x/llama3.2-typhoon2-1b-instruct"
    if model == "3b":
        model_id = "scb10x/llama3.2-typhoon2-3b-instruct"

    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี", model_id=model_id)
    
    def generate():
        for chunk in llm.ask_stream(prompt):
            print(chunk)  # ดูผลลัพธ์ใน console
            yield chunk + "\n"  # ส่ง chunk ออกไปทีละชิ้น

    return StreamingResponse(generate(), media_type="text/plain")