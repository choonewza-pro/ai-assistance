from fastapi import APIRouter, Query
from src.utils.ask_website import AskWebsite

router = APIRouter()

@router.get("/ask-website")
def ask_website(
    url: str = Query(..., description="The URL of the website to query"),
    targetClassName: str = Query(..., description="The target class name to extract content from"),
    question: str = Query(..., description="The question to ask the website"),
    clearOldData: bool = Query(False, description="Clear old data before ingesting new data")
):
    answer = "answer"
    prompt = "prompt"
    ask_website_instance = AskWebsite(url=url, targetClassName=targetClassName, clearOldData=clearOldData)
    answer, prompt = ask_website_instance.ask(question=question)
    return {
        "success": True,
        "result":{
            "answer": answer,
            "prompt": prompt,
        },
        "input":{
            "url": url,
            "targetClassName": targetClassName,
            "question": question,
            "clearOldData": clearOldData
        }
    }
