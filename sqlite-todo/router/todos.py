"""Todos file"""

from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from src.database import SessionLocal
from src.models import Todos
from router.auth import user_dependency

router = APIRouter(prefix="/todos", tags=["todos"])


class TodoRequest(BaseModel):
    """Model for Todo Request

    Args:
        BaseModel: pydantic model
    """

    task: str = Field(min_length=1, max_length=101)
    completed: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {"example": {"task": "Study", "completed": False}}
    }


def get_db():
    """get db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    """Function to get all todos

    Returns:
        array: All the todos
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return db.query(Todos).filter(Todos.owner_id == user.get("user_id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_single_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    """Function to get a single todo

    Returns:
        Todo: Return a single todo
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    todo = (
        db.query(Todos)
        .filter(Todos.todo_id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo does not exist")

    return {"todo": todo}


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def post_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    """Function to post a todo

    Args:
        todo (TodoRequest): todo

    Returns:
        string: Returns a message
    """

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    created_todo = Todos(**todo.model_dump(), owner_id=user.get("user_id"))

    db.add(created_todo)
    db.commit()

    return {"message": "Todo created successfully!"}


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo: TodoRequest,
    todo_id: int = Path(gt=0),
):
    """Function to update a todo

    Returns:
        todo_id: Id of the todo
        Todo: Return a single todo
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    found_todo = (
        db.query(Todos)
        .filter(Todos.todo_id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )

    if found_todo is None:
        raise HTTPException(status_code=404, detail="Todo does not exist")

    found_todo.task = todo.task  # type: ignore
    found_todo.completed = todo.completed  # type: ignore

    db.add(found_todo)
    db.commit()

    return {"message": "Todo updated successfully!"}


@router.delete("/delete/${todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    """Function to delete a todo

    Args:
        todo_id (int): todo todo_id

    Returns:
        string: Returns a message
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    found_todo = (
        db.query(Todos)
        .filter(Todos.todo_id == todo_id)
        .filter(Todos.owner_id == user.get("user_id"))
        .first()
    )

    if found_todo is None:
        raise HTTPException(status_code=404, detail="Todo does not exist")

    db.query(Todos).filter(Todos.todo_id == todo_id).delete()
    db.commit()

    return {"message": "Todo deleted successfully!"}
