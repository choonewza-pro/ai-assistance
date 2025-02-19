
- docker compose up -d ollama

- docker compose exec ollama ollama pull deepseek-r1:8b
- docker compose exec ollama ollama run deepseek-r1:8b

- docker compose exec ollama ollama pull deepseek-r1:32b
- docker compose exec ollama ollama run deepseek-r1:32b

- docker compose down -v