from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    completed: bool

# In-memory storage of to-do items
to_do_list: List[Item] = []

@app.get("/todos/", response_model=List[Item])
async def read_todos():
    return to_do_list

@app.post("/todos/", response_model=Item)
async def create_todo(item: Item):
    to_do_list.append(item)
    return item

@app.put("/todos/{item_id}", response_model=Item)
async def update_todo(item_id: int, item: Item):
    if item_id >= len(to_do_list):
        raise HTTPException(status_code=404, detail="Item not found")
    to_do_list[item_id] = item
    return item

@app.delete("/todos/{item_id}")
async def delete_todo(item_id: int):
    if item_id >= len(to_do_list):
        raise HTTPException(status_code=404, detail="Item not found")
    to_do_list.pop(item_id)
    return {"detail": "Item deleted"}