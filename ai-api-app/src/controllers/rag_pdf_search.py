import time
import os
from fastapi import APIRouter, Query
from src.utils.rag_utils import RagUtils

router = APIRouter()

@router.get("/rag-pdf-search")
def rag_pdf_search(
    question: str = Query(..., description="The URL of the website to query"),
):
    start_time = time.time()

    ragUtils = RagUtils(embeddings_dir="./chroma-pdfs")
    vector_store = ragUtils.loadVectorStore();
    vector_store_details = {
        "embedding_model": ragUtils.model_name,
    }

    retriever = ragUtils.getRetriever(vector_store=vector_store)
    retrieved_docs = retriever.invoke(question)
    
    # Convert retrieved_docs to a JSON-serializable format
    retrieved_docs_json = [{"content": doc.page_content, "metadata": doc.metadata} for doc in retrieved_docs]
    
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "retrieved_docs": retrieved_docs_json,
        "vector_store_details": vector_store_details,
    }