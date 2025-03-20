# เข้าใช้ env
python -m venv env
source env/bin/activate  

# install lib fastapi
pip install fastapi uvicorn

# Run Test
uvicorn src.main:app --reload

# export pip libraries
pip freeze > requirements.txt

# Install AI Libraries
pip install transformers torch accelerate

pip install -U langchain langchain_huggingface langchain-chroma langchain_community sentence-transformers langchain_huggingface langchain_core chromadb  pypdf PyMuPDF pdfplumber

pip install -U ipywidgets

pip install -U requests beautifulsoup4 langchain-community langchain-text-splitters langchain-chroma langchain_ollama 

pip install python-multipart

pip install llama-index llama-index-embeddings-huggingface