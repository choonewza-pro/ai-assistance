import os
import bs4
import requests
import shutil 
import urllib.request
from typing import List
import torch
import urllib.request
import pickle
import nest_asyncio
import json
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.opensearch import OpensearchVectorStore, OpensearchVectorClient
from llama_index.core.vector_stores.types import VectorStoreQueryMode

class OpenSearchService:
    def __init__(self,index_name: str):
        self.index_name = index_name
        self.original_get = requests.get
        self.model_name = "BAAI/bge-m3"
        self.model_kwargs = {'device': 'cpu'}
        self.encode_kwargs = {'normalize_embeddings': False}

    