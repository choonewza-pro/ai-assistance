# 1. Start Docker
- docker compose up -d ollama

# 2. Start LLM Model
- docker compose exec ollama ollama pull deepseek-r1:8b
- docker compose exec ollama ollama pull all-minilm
- docker compose exec ollama ollama pull nomic-embed-text
- docker compose exec -d ollama ollama run deepseek-r1:8b

# Other Commands
- docker exec -it ollama /bin/bash
- docker compose down -v
- docker system prune -a



