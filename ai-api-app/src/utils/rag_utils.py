import os
import bs4
import requests
import shutil 
from typing import List
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.retrievers import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from pypdf import PdfReader

class RagUtils:
    def __init__(self,embeddings_dir: str):
        self.embeddings_dir = embeddings_dir
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
    
    def splitText(self, text: str, chunk_size: int, chunk_overlap: int, metadataSource: str):
        """
        Split the input text into smaller chunks using RecursiveCharacterTextSplitter.
        """
        documents = [Document(page_content=text, metadata={"source": metadataSource})]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            strip_whitespace=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split text into {len(chunks)} chunks.")
        return chunks

    #splitDocuments
    def splitDocuments(self, documents: Document, chunk_size: int, chunk_overlap: int):
        """
        Split the input documents into smaller chunks using RecursiveCharacterTextSplitter.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            strip_whitespace=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split text into {len(chunks)} chunks.")
        return chunks

    def ingest(self, split_docs: List[Document]):
        """
        Ingest the list of Document chunks into a vector database.
        """
        embedding = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs
        )

        vector_store = None  # กำหนดค่าเริ่มต้นให้กับตัวแปร vector_store
        if os.path.exists(os.path.join(self.embeddings_dir, "chroma.sqlite3")):
            print("-- use Append data to vector store--")
            vector_store = Chroma(persist_directory=self.embeddings_dir, embedding_function=embedding)
            # สร้าง collection ใหม่โดยอัตโนมัติเมื่อเพิ่ม documents
            vector_store.add_documents(documents=split_docs)
        else:
            print("-- use New vector store--")
            os.makedirs(self.embeddings_dir, exist_ok=True)
            vector_store = Chroma.from_documents(documents=split_docs, embedding=embedding, persist_directory=self.embeddings_dir)

        print("-- Ingest to Vector Database Success ---")
        return vector_store

    def deleteVectorDatabase(self):
        """
        ลบข้อมูลเก่าในไดเรกทอรี embeddings
        """
        if os.path.exists(self.embeddings_dir):
            shutil.rmtree(self.embeddings_dir)
            print(f"Vector database at {self.embeddings_dir} deleted successfully.")
        else:
            print(f"Vector database at {self.embeddings_dir} does not exist.")

    def loadVectorStore(self):
        """
        Load the vector store from the specified embeddings directory.
        """
        if os.path.exists(os.path.join(self.embeddings_dir, "chroma.sqlite3")):
            embedding = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=self.model_kwargs,
                encode_kwargs=self.encode_kwargs
            )
            vector_store = Chroma(persist_directory=self.embeddings_dir, embedding_function=embedding)
            print(f"Vector store loaded from {self.embeddings_dir}.")
            return vector_store
        else:
            print(f"Vector store at {self.embeddings_dir} does not exist.")
            return None

    def deleteDocumentByIds(self, document_ids: List[str]):
        """
        ลบเอกสารใน Chroma vector store ตาม document_ids ที่กำหนด
        """
        if os.path.exists(os.path.join(self.embeddings_dir, "chroma.sqlite3")):
            vector_store = Chroma(persist_directory=self.embeddings_dir, embedding_function=HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=self.model_kwargs,
                encode_kwargs=self.encode_kwargs
            ))
            vector_store.delete(document_ids=document_ids)
            print(f"Documents with IDs {document_ids} deleted successfully.")
        else:
            print(f"Vector store at {self.embeddings_dir} does not exist.")

    def deleteAllDocuments(self):
        """
        ลบเอกสารทั้งหมดใน Chroma vector store
        """
        if os.path.exists(os.path.join(self.embeddings_dir, "chroma.sqlite3")):
            vector_store = Chroma(persist_directory=self.embeddings_dir, embedding_function=HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=self.model_kwargs,
                encode_kwargs=self.encode_kwargs
            ))
            vector_store.delete()
            print("All documents deleted successfully.")
        else:
            print(f"Vector store at {self.embeddings_dir} does not exist.")
    
    def resetAllDocuments(self):
        """
        ลบเอกสารทั้งหมดใน Chroma vector store
        """
        if os.path.exists(os.path.join(self.embeddings_dir, "chroma.sqlite3")):
            vector_store = Chroma(persist_directory=self.embeddings_dir, embedding_function=HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs=self.model_kwargs,
                encode_kwargs=self.encode_kwargs
            ))
            vector_store.reset_collection()
            print("All documents reset successfully.")
        else:
            print(f"Vector store at {self.embeddings_dir} does not exist.")

    def getRetriever(self, vector_store: Chroma):
        """
        Get a retriever from the vector store for similarity search.
        """
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        return retriever

    def genPrompt(self, question: str, retriever: BaseRetriever, role: str = "คุณเป็นผู้ช่วยตอบคำถามแบบสุภาพ"):
        """
        Generate a prompt based on the retrieved documents for the given question.
        """
        retrieved_docs = retriever.invoke(question)
        context = ' '.join([doc.page_content for doc in retrieved_docs])
        prompt = f"""
                {role} 
                คำถาม: {question}
                บริบท: {context} 
                กรุณาตอบคำถามโดยสรุปข้อมูลที่เกี่ยวข้อง
            """
        return prompt
    
    def loadDocumentsFromWebsite(self, url: str, targetClassName: str):
        """
        Load content from a website using the specified target class name.
        """
        requests.get = self.patched_get
        bs4_strainer = bs4.SoupStrainer(class_=targetClassName)
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs={"parse_only": bs4_strainer},
        )
        docs = loader.load()
        requests.get = self.original_get
        return docs
    
    def listPdfFiles(self, directory: str):
        """
        List all PDF files in the specified directory.
        """
        pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
        pdf_details = []
        
        for pdf_file in pdf_files:
            file_path = os.path.join(directory, pdf_file)
            file_size = os.path.getsize(file_path)
            
            with open(file_path, "rb") as f:
                pdf_reader = PdfReader(f)
                num_pages = len(pdf_reader.pages)
            
            file_info = {
                "file_name": pdf_file,
                "num_pages": num_pages,
                "file_size": file_size
            }
            
            pdf_details.append(file_info)
        return pdf_files, pdf_details
    
    def loadDocumentFromPdfFile(self, file_path: str):
        """
        Load a document from a PDF file.
        """
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        return docs
    
    def loadDocumentsFromPdfFiles(self, directory:str):
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