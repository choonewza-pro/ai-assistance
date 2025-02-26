import os
import bs4
import requests
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.retrievers import BaseRetriever

class RagUtils:
    def __init__(self):
        self.original_get = requests.get

    def patched_get(self, url, *args, **kwargs):
        """
        Patch the requests.get method to use a custom User-Agent header.
        """
        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        return self.original_get(url, headers=headers, *args, **kwargs)

    def textSplitter(self, text: str):
        """
        Split the input text into smaller chunks using RecursiveCharacterTextSplitter.
        """
        documents = [Document(page_content=text, metadata={"source": "website.txt"})]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=51,
            length_function=len,
            strip_whitespace=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split text into {len(chunks)} chunks.")
        return chunks

    def documentsSplitter(self, documents: Document):
        """
        Split the input documents into smaller chunks using RecursiveCharacterTextSplitter.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=51,
            length_function=len,
            strip_whitespace=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split text into {len(chunks)} chunks.")
        return chunks

    def ingest(self, chunks: List[Document], embeddings_dir: str):
        """
        Ingest the list of Document chunks into a vector database.
        """
        model_name = "BAAI/bge-m3"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        
        embedding = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        if os.path.exists(os.path.join(embeddings_dir, "chroma.sqlite3")):
            print("--append data to vector store--")
            vector_store = Chroma(persist_directory=embeddings_dir, embedding_function=embedding)
            vector_store.add_documents(documents=chunks)
        else:
            print("--new vector store--")
            os.makedirs(embeddings_dir, exist_ok=True)
            Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=embeddings_dir)

        print("--- Ingest to Vector Database Success ---")

    def loadContentFromWebsite(self, url: str, targetClassName: str):
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

    def loadVectorStore(self, embeddings_dir: str):
        """
        Load the vector store from the specified embeddings directory.
        """
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

    def getRetriever(self, vector_store: Chroma):
        """
        Get a retriever from the vector store for similarity search.
        """
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        return retriever

    def genPrompt(self, question: str, retriever: BaseRetriever):
        """
        Generate a prompt based on the retrieved documents for the given question.
        """
        retrieved_docs = retriever.invoke(question)
        context = ' '.join([doc.page_content for doc in retrieved_docs])
        prompt = f"""
            <s> [Instructions] 
                    You are a friendly assistant. Answer the question based only on the following context. 
                    If you don't know the answer, then reply, No Context available for this question.
                [/Instructions] 
            </s> 
            [Instructions] 
                Question: {question}
                Context: {context} 
                Answer:
            [/Instructions]
            """
        return prompt