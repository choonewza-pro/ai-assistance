from fastapi import APIRouter, Query
from src.utils.ask_pdf import AskPDF

router = APIRouter()

@router.get("/ask-pdf")
def ask_pdf(
    pdf_path: str = Query(..., description="The path of the PDF file to query"),
    question: str = Query(..., description="The question to ask the website"),
    clearOldData: bool = Query(False, description="Clear old data before ingesting new data")
):
    ask_pdf_instance = AskPDF(pdf_path=pdf_path, clearOldData=clearOldData)
    answer, prompt = ask_pdf_instance.ask(question=question)
    return {
        "success": True,
        "result":{
            "answer": answer,
            "prompt": prompt,
        },
        "input":{
            "pdf_path": pdf_path,
            "question": question,
            "clearOldData": clearOldData
        }
    }
