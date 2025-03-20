from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

todos = []

class Todo(BaseModel):
    id: int
    item: str
    
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return {"message": "Todo not found"}

@app.get("/time")
async def get_time():
    return {"time": datetime.utcnow().isoformat() + "Z"}


@app.get("/todos")
async def get_todos():
    return {"todos": todos}

@app.post("/todos")
async def create_todos(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created successfully"}