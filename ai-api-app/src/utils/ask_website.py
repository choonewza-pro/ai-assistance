from src.utils.rag_utils import RagUtils
from src.utils.typhoon_2_assistant import Typhoon2Assistant

class AskWebsite:
    def __init__(self, url: str, targetClassName: str, clearOldData: bool = False):
        self.url = url
        self.targetClassName = targetClassName
        self.regUtils = RagUtils(embeddings_dir="./embeddings-load-website")

        if clearOldData:
            self.regUtils.deleteAllDocuments()
        
        self.ingest();
             
    def ingest(self):
        documents = self.regUtils.loadContentFromWebsite(
            url=self.url,
            targetClassName=self.targetClassName
        )
        chunks = self.regUtils.documentsSplitter(
            documents=documents, 
            chunk_size=512, 
            chunk_overlap=51
        )
        self.regUtils.ingest(
            chunks=chunks,
        )
        vectorstore = self.regUtils.loadVectorStore()
        retriever = self.regUtils.getRetriever(vectorstore)
        self.retriever = retriever
    
    def ask(self, question: str):
        prompt = self.regUtils.genPrompt(question=question, retriever=self.retriever)
        llm = Typhoon2Assistant()
        answer = llm.ask(prompt)
        return answer, prompt


        