# New Install FastAPI
python -m venv env
source env/bin/activate  
pip install fastapi uvicorn

# Run Test
uvicorn src.main:app --reload

# export pip libraries
pip freeze > requirements.txt

# Install AI Libraries
pip install -U requests beautifulsoup4 langchain-community langchain-text-splitters langchain-chroma langchain_ollama pypdf