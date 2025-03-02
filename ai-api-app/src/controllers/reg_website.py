import os
import bs4
import requests
from fastapi import APIRouter
from langchain_community.document_loaders import WebBaseLoader
from src.utils.requests_utils import patched_get
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM

router = APIRouter()

base_url = "http://172.17.0.1:11434/"

# base_url = "http://localhost:11434/"

@router.get("/reg-website")
def reg_website():
    # ตั้งค่าให้ Ollama ใช้เซิร์ฟเวอร์ที่รันอยู่บนเครื่องอื่น
    os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

    # แทนที่ requests.get ด้วย patched_get
    original_get = requests.get
    requests.get = patched_get

    # ใช้ WebBaseLoader ตามปกติ
    bs4_strainer = bs4.SoupStrainer(class_="EntryReaderInner")
    loader = WebBaseLoader(
        web_paths=("https://www.sanook.com/news/9738102/",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()

    # คืนค่า requests.get กลับเป็นปกติ (ถ้าต้องการ)
    requests.get = original_get

    # print(docs)

    # chunking 1
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, 
        chunk_overlap=51, 
        length_function=len,
        strip_whitespace=True,
    )
    all_splits = text_splitter.split_documents(docs)

    # chunking by bge-m3
    local_embeddings = OllamaEmbeddings(
        model="bge-m3",
        base_url=base_url
    )


    # สร้างไดเรกทอรีสำหรับบันทึก embeddings
    embeddings_dir = "./embeddings"
    os.makedirs(embeddings_dir, exist_ok=True)

    # สร้าง vectorstore และบันทึก embeddings ลงในไฟล์
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=local_embeddings, persist_directory=embeddings_dir)
    vectorstore.persist()

    question = "มีเมืองอะไรบ้างที่จะถูกดาวเคราะห์ชน?"

    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    retrieved_docs = retriever.invoke(question)

    # print(retrieved_docs)

    context = ' '.join([doc.page_content for doc in retrieved_docs])

    llm = OllamaLLM(
        model="deepseek-r1:7b",
        base_url=base_url
    )

    prompt = f"""Answer the question according to the context given very briefly (English are allowed):
            Question: {question}.
            Context: {context}.
            Answer: 
    """

    print(prompt)

    response = llm.invoke(prompt)

    return {
        "success": True,
        "prompt": prompt,
        "response":response
    }