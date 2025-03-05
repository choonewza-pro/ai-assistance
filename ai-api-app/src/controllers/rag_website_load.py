import time
from fastapi import APIRouter, Query
from src.utils.ask_websites import AskWebs

router = APIRouter()

@router.get("/rag-website-load")
def rag_website_load(
    url: str = Query(..., description="The URL of the website to query"),
    targetClassName: str = Query(..., description="The target class name to extract content from"),
):
    start_time = time.time()

    askWebs = AskWebs()

    result = askWebs.import_website(
        url=url,
        targetClassName=targetClassName
    )

    end_time = time.time()
    execution_time = end_time - start_time

    return {
        "execution_time": execution_time,
        "vector_store_details": result["vector_store_details"],
        "chunks_created": result["chunks_created"],
        "url": url,
        "targetClassName": targetClassName,
        "documents": result["documents"],
    }