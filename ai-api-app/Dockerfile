FROM python:3.13.2-bookworm

WORKDIR /code 

COPY requirements.txt .  

RUN pip install --no-cache-dir --upgrade -r requirements.txt 

COPY . . 

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"] 