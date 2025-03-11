"""Todos file"""

from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from src.database import SessionLocal
from src.models import Todos
from router.auth import user_dependency

router = APIRouter(prefix="/admin", tags=["admin"])


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
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return db.query(Todos).all()


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
    if user is None or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    found_todo = db.query(Todos).filter(Todos.todo_id == todo_id).first()

    if found_todo is None:
        raise HTTPException(status_code=404, detail="Todo does not exist")

    db.query(Todos).filter(Todos.todo_id == todo_id).delete()
    db.commit()

    return {"message": "Todo deleted successfully!"}
