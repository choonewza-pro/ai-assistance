import os
import bs4
import requests
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document  # นำเข้า Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.retrievers import BaseRetriever

original_get = requests.get


def patched_get(url, *args, **kwargs):
    headers = kwargs.pop("headers", {})
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    return original_get(url, headers=headers, *args, **kwargs)

def textSplitter(text: str):
    # สร้าง Document
    documents = [Document(page_content=text, metadata={
        "source":"website.txt"
    })]
    
    # Split the text by char
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=51,
        length_function=len,
        strip_whitespace=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split text into {len(chunks)} chunks.")
    return chunks

def documentsSplitter(documents: Document):
    # Split the text by char
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=51,
        length_function=len,
        strip_whitespace=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split text into {len(chunks)} chunks.")
    return chunks

def ingest(chunks: List[Document], embeddings_dir:str):
    """
    ฟังก์ชันที่รับรายการของ Document (chunks) และนำไปสร้าง Vector database
    """

    model_name = "BAAI/bge-m3"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embedding = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

   # ตรวจสอบว่ามี vector store อยู่แล้วหรือไม่
    if os.path.exists(os.path.join(embeddings_dir, "chroma.sqlite3")):
        print("--append data to vector store--")
        # โหลด vector store ที่มีอยู่
        vector_store = Chroma(persist_directory=embeddings_dir, embedding_function=embedding)
        # เพิ่มเอกสารใหม่
        vector_store.add_documents(documents=chunks)
    else:
        print("--new vector store--")
        # สร้างไดเรกทอรีสำหรับบันทึก embeddings
        os.makedirs(embeddings_dir, exist_ok=True)
        # สร้าง vector store ใหม่และบันทึก embeddings ลงในไฟล์
        Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=embeddings_dir)

    print("--- Ingest to Vector Database Success ---")

def loadContentFromWebsite(url: str, targetClassName: str):
    requests.get = patched_get  # ใช้ patched version ของ requests.get
    bs4_strainer = bs4.SoupStrainer(class_=targetClassName)
    loader = WebBaseLoader(
        web_paths=(url,), # , ที่อยู่ในวงเล็บสำคัญนะห้ามลบ
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    # คืนค่า requests.get กลับเป็นปกติ (ถ้าต้องการ)
    requests.get = original_get
    
    return docs

def loadVectorStore(embeddings_dir: str):
    model_name = "BAAI/bge-m3"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    
    embedding = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    vector_store = Chroma(persist_directory=embeddings_dir, embedding_function=embedding)
    print("--Vector Store Loaded--")
    return vector_store

def getRetriever(vector_store: Chroma):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return retriever

def genPrompt(question : str, retriever: BaseRetriever):
    retrieved_docs = retriever.invoke(question )
    context = ' '.join([doc.page_content for doc in retrieved_docs])
    prompt = f"""
        <s> [Instructions] 
                You are a friendly assistant. Answer the question based only on the following context. 
                If you don't know the answer, then reply, No Context availabel for this question.
            [/Instructions] 
        </s> 
        [Instructions] 
            Question: {question}
            Context: {context} 
            Answer:
        [/Instructions]
        """
    return prompt