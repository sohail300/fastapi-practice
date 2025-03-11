"""Todos file"""

from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from src.database import SessionLocal
from src.models import Users
from router.auth import user_dependency, bcrypt_context

router = APIRouter(prefix="/user", tags=["user"])


class UpdateRequest(BaseModel):
    age: int = Field(gt=0)


def get_db():
    """get db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/details", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    """Function to get all todos

    Returns:
        array: All the todos
    """
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return db.query(Users).filter(Users.user_id == user.get("user_id")).first()


@router.put("/update/", status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(
    user: user_dependency,
    db: db_dependency,
    profile_update: UpdateRequest,
):
    """Function to update a todo"""

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    found_user = db.query(Users).filter(Users.user_id == user.get("user_id")).first()

    if found_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    found_user.age = profile_update.age  # type: ignore

    db.add(found_user)
    db.commit()

    return {"message": "Profile updated successfully!"}


@router.put("/change_password/{new_password}", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    new_password: str = Path(min_length=6, max_length=101),
):
    """Function to delete a todo

    Args:
        new_password (str): New Password

    Returns:
        string: Returns a message
    """
    print(new_password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    found_user = db.query(Users).filter(Users.user_id == user.get("user_id")).first()

    if found_user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    found_user.hashed_password = bcrypt_context.hash(new_password)

    db.add(found_user)
    db.commit()

    return {"message": "Todo deleted successfully!"}
