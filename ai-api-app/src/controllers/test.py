import time
import os
from fastapi import APIRouter, Query
from src.utils.rag_service import RagService

router = APIRouter()

@router.get("/test")
def test():
    start_time = time.time()

   

    current_dir = os.getcwd()
    md_directory = current_dir + "/public/md_files"

    if not os.path.exists(md_directory):
        os.makedirs(md_directory)

    ragService = RagService()

    documents = ragService.load_markdowns(directory=md_directory)
    nodes = ragService.split_by_markdown(documents=documents)
    # nodes = ragService.split_by_sentent(documents=documents, chunk_size=512, chunk_overlap=50)

    end_time = time.time()
    
    execution_time = end_time - start_time

    return {
       "action":"test",
       "execution_time1": execution_time,
       "len_nodes" : len(nodes),
       "nodes": nodes,
    }