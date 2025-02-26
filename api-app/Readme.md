https://stackpython.co/tutorial/python-application-docker-container

# CREATE
```
$ mkdir todo-app
$ cd todo-app
$ python -m venv env
$ source env/bin/activate  
(env) $ pip install fastapi uvicorn
```

# ทดสอบแบบ local
```
(env) $ uvicorn main:app --reload
```

# ทำ Dockerfile
```
$ pip freeze > requirements.txt
```

# Run Docker Container
```
$ docker compose up -d
```



pip install -U requests beautifulsoup4 langchain-community langchain-text-splitters langchain-chroma langchain_ollama pypdf
