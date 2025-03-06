from src.utils.rag_utils import RagUtils

class AskPDFs:
    def __init__(self):
        self.ragUtils = RagUtils(embeddings_dir="./chroma-pdfs")
        
    def list_pdfs(self, pdf_directory: str):
        pdf_files, pdf_details = self.ragUtils.listPdfFiles(directory=pdf_directory)
        return {
            "pdf_files": pdf_files,
            "pdf_details": pdf_details,
        }
    def resetAllDocuments(self):
        self.ragUtils.resetAllDocuments()

    def import_pdf(self, file_path:str):
        documents = self.ragUtils.loadDocumentFromPdfFile(file_path=file_path)
        split_docs = self.ragUtils.splitDocuments(documents=documents, chunk_size=512, chunk_overlap=54)
        self.ragUtils.ingest(split_docs=split_docs)
        vector_store_details = {
            "embedding_model": self.ragUtils.model_name,
        }
        return {
            "vector_store_details": vector_store_details,
            "chunks_created": len(split_docs),
        }

    def load_pdfs(self, pdf_directory: str):
        # current_dir = os.getcwd()
        # pdf_directory = current_dir + "/public/pdf_files"
        pdf_files, pdf_details = self.ragUtils.listPdfFiles(directory=pdf_directory)    
        documents = self.ragUtils.loadDocumentsFromPdfFiles(directory=pdf_directory)
        split_docs = self.ragUtils.splitDocuments(documents=documents, chunk_size=512, chunk_overlap=54)
        self.ragUtils.resetAllDocuments()
        self.ragUtils.ingest(split_docs=split_docs)
        vector_store_details = {
            "embedding_model": self.ragUtils.model_name,
        }
        return {
            "vector_store_details": vector_store_details,
            "chunks_created": len(split_docs),
            "pdf_files": pdf_files,
            "pdf_details": pdf_details,
        }

    def search_pdf_chunks(self, question: str):
        vector_store = self.ragUtils.loadVectorStore();

        if vector_store is None:
            return None
        
        vector_store_details = {
            "embedding_model": self.ragUtils.model_name,
        }
        retriever = self.ragUtils.getRetriever(vector_store=vector_store)
        retrieved_docs = retriever.invoke(question)
        # Convert retrieved_docs to a JSON-serializable format
        retrieved_docs_json = [{"content": doc.page_content, "metadata": doc.metadata} for doc in retrieved_docs]

        return {
            "retrieved_docs": retrieved_docs_json,
            "vector_store_details": vector_store_details,
        }
    
    def genPrompt(self, question: str):
        vector_store = self.ragUtils.loadVectorStore();

        if vector_store is None:
            return None
        
        vector_store_details = {
            "embedding_model": self.ragUtils.model_name,
        }
        retriever = self.ragUtils.getRetriever(vector_store=vector_store)
        role = "คุณเป็นผู้ช่วยอัจฉริยะที่สามารถตอบคำถามเกี่ยวกับเนื้อหาของเอกสาร PDF ได้ดี"
        prompt = self.ragUtils.genPrompt(question=question, retriever=retriever,role=role)

        retrieved_docs = retriever.invoke(question)
        # Convert retrieved_docs to a JSON-serializable format
        retrieved_docs_json = [{"content": doc.page_content, "metadata": doc.metadata} for doc in retrieved_docs]
    
        prompt = self.ragUtils.genPrompt(question=question, retriever=retriever)

        return {
            "prompt": prompt,
            "system_role": role,
            "retrieved_docs": retrieved_docs_json,
            "vector_store_details": vector_store_details,
        }


        