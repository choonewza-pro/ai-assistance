import os
import bs4
import requests
import shutil 
import urllib.request
from typing import List
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from pypdf import PdfReader
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import MarkdownNodeParser, SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class RagService:
    def __init__(self):
        self.original_get = requests.get
        self.model_name = "BAAI/bge-m3"
        self.model_kwargs = {'device': 'cpu'}
        self.encode_kwargs = {'normalize_embeddings': False}

    def patched_get(self, url, *args, **kwargs):
        """
        Patch the requests.get method to use a custom User-Agent header.
        """
        user_agent =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        os.environ["USER_AGENT"] =user_agent
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = user_agent
        return self.original_get(url, headers=headers, *args, **kwargs)
    
    def load_pdf(self, file_path: str):
        """
        Load a document from a PDF file.
        """
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return docs
    
    def load_pdfs(self, directory:str):
        documents = []
        # Loop ผ่านไฟล์ทั้งหมดใน directory
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(directory, filename)
                try:
                    # โหลด PDF โดยใช้ PyPDFLoader
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    documents.extend(docs)
                    print(f"Loaded: {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
        return documents
    
    def load_markdowns(self, directory:str):
        documents = []
        # Loop ผ่านไฟล์ทั้งหมดใน directory
        reader = SimpleDirectoryReader(
            input_dir=directory,
            recursive=True,
            required_exts=[".md", ".markdown"]
        )
        documents = reader.load_data()
        print(f"โหลดเอกสาร {len(documents)} ไฟล์สำเร็จ")
        return documents
    
    def split_by_sentent(self, documents: List[Document], chunk_size: int, chunk_overlap: int):
        """
        Split the input documents into smaller chunks using SentenceSplitter.
        """
        sentence_splitter = SentenceSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        nodes = sentence_splitter.get_nodes_from_documents(documents)
        print(f"Split documents into {len(nodes)} nodes by sentent.")
        return nodes
    
    def split_by_markdown(self, documents: List[Document], ):
        """
        Split the input documents into smaller chunks using MarkdownNodeParser.
        """
        md_parser = MarkdownNodeParser()
        nodes = md_parser.get_nodes_from_documents(documents)
        print(f"Split documents into {len(nodes)} nodes by markdown.")
        return nodes