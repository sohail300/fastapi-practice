import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    task: str

todos=[];

@app.get('/')
def root():
    return {"message": "Healthy Server!"}

@app.get('/todos')
def get_all_todos():
    return {"todos": todos}

@app.post('/todo')
def post_todo(todo: Todo):
    print(todo.dict())
    todo_dict = todo.dict()
    todo_dict.update({"id": len(todos)+1})
    todos.append(todo_dict)
    return {"message": f"Todo created successfully with id {len(todos)}"}

@app.delete('/todo/${todo_id}')
def delete_todo(todo_id: int):
    deleted_todo = todos.pop(todo_id-1);
    return {"message": f"Deleted todo {deleted_todo}"}
