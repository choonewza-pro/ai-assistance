from src.utils.rag_utils import RagUtils
from src.utils.typhoon_2_assistant import Typhoon2Assistant

class AskPDF:
    def __init__(self, pdf_path: str, clearOldData: bool = False):
        self.pdf_path = pdf_path
        self.regUtils = RagUtils(embeddings_dir="./embeddings-load-pdf")

        if clearOldData:
            self.regUtils.deleteAllDocuments()
        
        self.ingest();
             
    def ingest(self):
        documents = self.regUtils.loadContentFromPDF(
            pdf_path=self.pdf_path,
        )
        split_docs = self.regUtils.splitDocuments(
            documents=documents, 
            chunk_size=512, 
            chunk_overlap=51
        )
        self.regUtils.ingest(
            split_docs=split_docs,
        )
        vectorstore = self.regUtils.loadVectorStore()
        retriever = self.regUtils.getRetriever(vectorstore)
        self.retriever = retriever
    
    def ask(self, question: str):
        prompt = self.regUtils.genPrompt(question=question, retriever=self.retriever)
        llm = Typhoon2Assistant()
        answer = llm.ask(prompt)
        return answer, prompt


        