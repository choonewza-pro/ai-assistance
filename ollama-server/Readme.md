# 1. Start Docker
- docker compose up -d

# 2. Start LLM Model

- docker compose exec ollama ollama pull scb10x/llama3.2-typhoon2-1b-instruct

- docker compose exec ollama ollama pull scb10x/llama3.2-typhoon2-3b-instruct
- docker compose exec -d ollama ollama run scb10x/llama3.2-typhoon2-3b-instruct

- docker compose exec ollama ollama pull promptnow/openthaigpt1.5-7b-instruct-q4_k_m
- docker compose exec -d ollama ollama run promptnow/openthaigpt1.5-7b-instruct-q4_k_m

- docker compose exec ollama ollama pull scb10x/llama3.2-typhoon2-t1-3b-research-preview
- docker compose exec -d ollama ollama run scb10x/llama3.2-typhoon2-t1-3b-research-preview

- docker compose exec ollama ollama pull deepseek-r1:1.5b
- docker compose exec ollama ollama pull bge-m3:latest
- docker compose exec -d ollama ollama run deepseek-r1:1.5b

- docker compose exec ollama ollama pull llama3.2:3b
- docker compose exec -d ollama ollama run llama3.2:3b

- docker compose exec ollama ollama pull qwen2.5:3b
- docker compose exec -d ollama ollama run qwen2.5:3b

# typhoon2 with Ollama
- docker compose exec -d ollama ollama pull hf.co/Float16-cloud/llama3.2-typhoon2-3b-instruct-gguf:IQ4_NL
- docker compose exec -d ollama ollama pull hf.co/Float16-cloud/llama3.2-typhoon2-1b-instruct-gguf:IQ4_NL


# Other Commands
- docker exec -it ollama /bin/bash
- docker compose down -v
- docker system prune -a


# คำสั่งตรวจสอบการรับรอง GPU
- docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

หากเห็นรายละเอียดของ GPU แสดงว่าพร้อมใช้งาน 🚀









