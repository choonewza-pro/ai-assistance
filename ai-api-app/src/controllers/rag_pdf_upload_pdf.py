import time
import os
from fastapi import APIRouter, File, UploadFile
from src.utils.ask_pdfs import AskPDFs

router = APIRouter()

@router.post("/rag-pdf-upload-pdf")
async def rag_pdf_upload_pdf(file: UploadFile = File(...)):
    start_time = time.time()
    
    askPDFs = AskPDFs()

    current_dir = os.getcwd()
    pdf_directory = os.path.join(current_dir, "public", "pdf_files")
    os.makedirs(pdf_directory, exist_ok=True)

    file_path = os.path.join(pdf_directory, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    
    result = askPDFs.import_pdf(file_path=file_path)

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "filename": file.filename,
        "execution_time": execution_time,
        "vector_store_details": result["vector_store_details"],
        "chunks_created": result["chunks_created"],
    }