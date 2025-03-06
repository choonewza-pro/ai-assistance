import time
import os
from fastapi import APIRouter, Query
from src.utils.ask_pdfs import AskPDFs

router = APIRouter()

@router.get("/rag-pdf-list-pdfs")
def rag_pdf_list_pdfs(
):
    start_time = time.time()
    
    askPDFs = AskPDFs()

    current_dir = os.getcwd()
    pdf_directory = current_dir + "/public/pdf_files"

    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
        
    result = askPDFs.list_pdfs(pdf_directory=pdf_directory)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "pdf_files": result["pdf_files"],
        "pdf_details": result["pdf_details"],
    }
