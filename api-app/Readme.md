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