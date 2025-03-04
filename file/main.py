import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    task: str

@app.get('/')
def root():
    return {"message": "Healthy Server!"}

@app.get('/todos')
def get_all_todos():
    try:
        with open('todos.txt', 'r') as file:
            content = json.loads(file.read())

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        content = []
    
    return {"todos": content}

@app.post('/todo')
def post_todo(todo: Todo):
    try:
        with open('todos.txt', 'r') as file:
            file_array = json.loads(file.read())
            
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        file_array = []
    
    length = len(file_array)
    todo_dict = todo.model_dump()
    todo_dict.update({"id": length+1})
    file_array.append(todo_dict)
    
    with open('todos.txt', 'w') as file:
        file.write(json.dumps(file_array))

    return {"message": f"Todo posted with id: {length+1}"}

@app.delete('/todo/${todo_id}')
def delete_todo(todo_id: int):
    try:
        with open('todos.txt', 'r') as file:
            file_array = json.loads(file.read())

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return {"message": "File is already empty!"}

    deleted_todo = file_array.pop(todo_id-1)

    with open('todos.txt', 'w') as file:
        file.write(json.dumps(file_array))

    return {"message": f"Deleted todo {deleted_todo}"}
