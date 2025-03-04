# 1. Start Docker
- docker compose up -d

# 2. Start LLM Model
- docker compose exec ollama ollama pull deepseek-r1:1.5b
- docker compose exec ollama ollama pull bge-m3:latest
- docker compose exec -d ollama ollama run deepseek-r1:1.5b

- docker compose exec ollama ollama pull llama3.2:3b
- docker compose exec -d ollama ollama run llama3.2:3b

- docker compose exec ollama ollama pull qwen2.5:3b
- docker compose exec -d ollama ollama run qwen2.5:3b

# typhoon2 with Ollama
- docker compose exec -d ollama ollama run hf.co/Float16-cloud/llama3.2-typhoon2-3b-instruct-gguf:IQ4_NL


# Other Commands
- docker exec -it ollama /bin/bash
- docker compose down -v
- docker system prune -a



