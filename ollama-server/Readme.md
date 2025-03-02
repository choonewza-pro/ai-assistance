# 1. Start Docker
- docker compose up -d

# 2. Start LLM Model
- docker compose exec ollama ollama pull deepseek-r1:1.5b
- docker compose exec ollama ollama pull bge-m3:latest
- docker compose exec -d ollama ollama run deepseek-r1:1.5b

# Other Commands
- docker exec -it ollama /bin/bash
- docker compose down -v
- docker system prune -a



