"""Module used to make a todo application"""

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Todo:  # pylint: disable=too-few-public-methods
    """Model for Todo"""

    todo_id: int | None
    task: str
    completed: bool

    def __init__(self, todo_id, task, completed):
        self.todo_id = todo_id
        self.task = task
        self.completed = completed


class TodoRequest(BaseModel):
    """Model for Todo Request

    Args:
        BaseModel: pydantic model
    """

    todo_id: int | None = Field(
        description="Not present in Post Todo", default=None, gt=0
    )
    task: str = Field(min_length=1, max_length=101)
    completed: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {"example": {"task": "Study", "completed": False}}
    }


todos = [Todo(todo_id=1, task="Wake Up", completed=True)]


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Health check function

    Returns:
        string: Returns Healthy Server
    """

    return {"message": "Healthy Server!"}


@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos():
    """Function to get all todos

    Returns:
        array: All the todos
    """

    return {"todos": todos}


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_single_todo(todo_id: int = Path(gt=0)):
    """Function to get a single todo

    Returns:
        Todo: Return a single todo
    """

    for todo in todos:
        if todo.todo_id == todo_id:
            return {"todo": todo}

    raise HTTPException(status_code=404, detail="Item does not exist")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def post_todo(todo: TodoRequest):
    """Function to post a todo

    Args:
        todo (TodoRequest): todo

    Returns:
        string: Returns a message
    """
    print(todo.model_dump())
    todo_dict = Todo(**todo.model_dump())
    todos.append(get_last_id(todo_dict))
    return {"message": f"Todo created successfully with todo_id {len(todos)}"}


@app.put("/todos", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo: TodoRequest):
    """Function to update a todo

    Returns:
        Todo: Return a single todo
    """

    for index, item in enumerate(todos):
        if item.todo_id == todo.todo_id and todo.todo_id is not None:
            todos[index] = Todo(**todo.model_dump())
            return {"message": "Todo updated"}

    raise HTTPException(status_code=404, detail="Item does not exist")


@app.delete("/todo/${todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int = Path(gt=0)):
    """Function to delete a todo

    Args:
        todo_id (int): todo todo_id

    Returns:
        string: Returns a message
    """

    for index, item in enumerate(todos):
        if item.todo_id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted"}

    raise HTTPException(status_code=404, detail="Item does not exist")


def get_last_id(todo: Todo):
    """gets the last id from the list of todos

    Parameters
    ----------
    todo : Todo
        it is the current todo given via post request
    """
    last_id = todos[-1].todo_id if todos and todos[-1].todo_id is not None else 0
    todo.todo_id = last_id + 1

    return todo
