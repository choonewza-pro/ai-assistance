from src.utils.rag_utils import RagUtils

class AskWebs:
    def __init__(self):
        self.ragUtils = RagUtils(embeddings_dir="./chroma-websites")
        

    def import_website(self, url: str, targetClassName: str):
        documents = self.ragUtils.loadDocumentsFromWebsite(
            url=url,
            targetClassName=targetClassName
        )
        split_docs = self.ragUtils.splitDocuments(documents=documents, chunk_size=512, chunk_overlap=54)
        self.ragUtils.ingest(split_docs=split_docs)
        vector_store_details = {
            "embedding_model": self.ragUtils.model_name,
        }
        return {
            "vector_store_details": vector_store_details,
            "chunks_created": len(split_docs),
            "documents": documents,
        }
    
    def resetAllDocuments(self):
        self.ragUtils.resetAllDocuments()

    def search_website_chunks(self, question: str):
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
        role = "คุณเป็นผู้ช่วยอัจฉริยะที่สามารถตอบคำถามได้ดี"
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


        