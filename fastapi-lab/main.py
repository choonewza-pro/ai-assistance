from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from typing import Union
from controllers.reg_website import router as reg_website_router

app = FastAPI()

@app.get("/hello")
def hello():
    return {"Message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id:int, q:Union[str, None]=None):
        return {"item_id": item_id, "q": q}


app.include_router(reg_website_router)