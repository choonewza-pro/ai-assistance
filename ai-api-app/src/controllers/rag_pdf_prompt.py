import time
import os
from fastapi import APIRouter, Query
from src.utils.ask_pdfs import AskPDFs

router = APIRouter()

@router.get("/rag-pdf-prompt")
def rag_pdf_prompt(
    question: str = Query(..., description="The URL of the website to query"),
):
    start_time = time.time()

    askPDFs = AskPDFs()
    result = askPDFs.genPrompt(question=question);

    def fix_thai_text(text):
        # แผนที่สำหรับแทนที่ตัวอักษรที่เสียหาย
        replacements = {
            "": "่",  # วรรณยุกต์ไม้เอก
            "": "้",  # วรรณยุกต์ไม้โท
            "": "้",  # วรรณยุกต์ไม้โท (บางกรณีอาจซ้ำ)
            "": "์",  # วรรณยุกต์การันต์
            "": "็",  # วรรณยุกต์ไม้ตรี
            "":"็", # วรรณยุกต์ไตคู้
            "": "๋",  # วรรณยุกต์ไม้จัดตาวา
            "ํ": "ำ",  # สระอำ
            # เพิ่มตามตัวอักษรที่เสียหายในข้อมูลของคุณ
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        return text

    prompt_fix = fix_thai_text(result["prompt"])

    end_time = time.time()
    execution_time = end_time - start_time

    response = {
        "execution_time": execution_time,
        "prompt": prompt_fix,
        "question": question,
        "retrieved_docs": result["retrieved_docs"],
        "vector_store_details": result["vector_store_details"],
    }
    
    

    
    return response