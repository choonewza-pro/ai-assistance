# New Install FastAPI
python -m venv env
source env/bin/activate  
pip install fastapi uvicorn
pip install transformers torch accelerate
pip install -U langchain langchain_huggingface langchain-chroma langchain_community sentence-transformers langchain_huggingface langchain_core chromadb ipywidgets pypdf

# Run Test
uvicorn src.main:app --reload

# export pip libraries
pip freeze > requirements.txt

# Install AI Libraries
pip install -U requests beautifulsoup4 langchain-community langchain-text-splitters langchain-chroma langchain_ollama pypdf