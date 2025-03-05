import time
import os
from fastapi import APIRouter
from src.utils.rag_utils import RagUtils

router = APIRouter()

@router.get("/rag-pdf-load")
def rag_pdf_load():
    start_time = time.time()

    ragUtils = RagUtils(embeddings_dir="./chroma-pdfs")
    current_dir = os.getcwd()
    pdf_directory = current_dir + "/public/pdf_files"

    pdf_files, pdf_details = ragUtils.listPdfFiles(directory=pdf_directory)

    documents = ragUtils.loadDocumentsFromPdfFiles(directory=pdf_directory)
    split_docs = ragUtils.splitDocuments(documents=documents, chunk_size=512, chunk_overlap=54)

    # Ensure the collection is initialized
    ragUtils.ingest(split_docs=split_docs)

    vector_store_details = {
        "embedding_model": ragUtils.model_name,
    }

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "vector_store_details": vector_store_details,
        "Total chunks created:": len(split_docs),
        "pdf_files": pdf_files,
        "pdf_details": pdf_details,
    }