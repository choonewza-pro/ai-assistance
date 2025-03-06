import time
import os
from fastapi import APIRouter
from src.utils.ask_pdfs import AskPDFs

router = APIRouter()

@router.post("/rag-pdf-reset")
def rag_pdf_reset():
    start_time = time.time()

    askPDFs = AskPDFs()

    current_dir = os.getcwd()
    pdf_directory = current_dir + "/public/pdf_files"

    askPDFs.resetAllDocuments()

    for file_name in os.listdir(pdf_directory):
        file_path = os.path.join(pdf_directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
    }