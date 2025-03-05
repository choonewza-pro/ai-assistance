import time
import os
from fastapi import APIRouter
from src.utils.rag_utils import RagUtils
from src.utils.ask_pdfs import AskPDFs

router = APIRouter()

@router.get("/rag-pdf-load")
def rag_pdf_load():
    start_time = time.time()

    askPDFs = AskPDFs()

    current_dir = os.getcwd()
    pdf_directory = current_dir + "/public/pdf_files"

    result = askPDFs.load_pdfs(pdf_directory=pdf_directory)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "vector_store_details": result["vector_store_details"],
        "chunks_created": result["chunks_created"],
        "pdf_files": result["pdf_files"],
        "pdf_details": result["pdf_details"],
    }