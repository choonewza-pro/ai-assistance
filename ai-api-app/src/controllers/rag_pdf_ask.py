import time
import os
from fastapi import APIRouter, Query
from src.utils.rag_utils import RagUtils
from src.utils.typhoon_2_assistant import Typhoon2Assistant

router = APIRouter()

@router.get("/rag-pdf-ask")
def rag_pdf_ask(
    question: str = Query(..., description="The URL of the website to query"),
    model: str = Query("1b", description="The model ID to use 1b or 3b")
):
    start_time = time.time()

    model_id = "scb10x/llama3.2-typhoon2-1b-instruct"

    if model == "3b":
        model_id ="scb10x/llama3.2-typhoon2-3b-instruct"

    ragUtils = RagUtils(embeddings_dir="./chroma-pdfs")
    vector_store = ragUtils.loadVectorStore();
    vector_store_details = {
        "embedding_model": ragUtils.model_name,
    }

    retriever = ragUtils.getRetriever(vector_store=vector_store)
    prompt = ragUtils.genPrompt(question=question, retriever=retriever)

    # # Remove extra spaces from the prompt
    # prompt = ' '.join(prompt.split())

    # Convert retrieved_docs to a JSON-serializable format
    retrieved_docs = retriever.invoke(question)
    retrieved_docs_json = [{"content": doc.page_content, "metadata": doc.metadata} for doc in retrieved_docs]

    llm = Typhoon2Assistant(system_content="คุณเป็นผู้ช่วยที่เป็นมิตร ตอบคำถามได้เป็นอย่างดี ช่วยเลือกคำตอบที่ดีจาก context ที่ให้",model_id=model_id)
    answer = llm.ask(prompt)
    
    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "answer": answer,
        "prompt": prompt,
        "model": model_id,
        "retrieved_docs": retrieved_docs_json,
        "vector_store_details": vector_store_details,
    }