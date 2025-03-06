import time
import os
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/rag-pdf-list-pdfs")
def rag_pdf_list_pdfs(
):
    start_time = time.time()
    
    askPDFs = AskPDFs()

    current_dir = os.getcwd()
    pdf_directory = current_dir + "/public/pdf_files"

    documents = askPDFs.list_pdfs(pdf_directory=pdf_directory)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "documents": documents,
    }
