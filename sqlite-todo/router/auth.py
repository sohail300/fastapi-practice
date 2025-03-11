"""Auth file"""

from typing import Annotated
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from starlette import status
from jose import jwt, JWTError
from src.database import SessionLocal
from src.models import Users


router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

ALGORITHM = "HS256"
SECRET_KEY = "5f362f45d567667712eb404d9315dfad"


def get_db():
    """get db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=101)
    password: str = Field(min_length=6, max_length=101)
    role: str = Field(min_length=1, max_length=20)
    age: int = Field(gt=0)


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    expires = datetime.now(timezone.utc) + expires_delta

    encode = {"username": username, "user_id": user_id, "role": role, "exp": expires}

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        username: str = payload.get("username")
        user_id: int = payload.get("user_id")
        role: int = payload.get("role")

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
            )

        return {"username": username, "user_id": user_id, "role": role}

    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        ) from exc


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_body: CreateUserRequest):
    user = Users(
        username=create_user_body.username,
        hashed_password=bcrypt_context.hash(create_user_body.password),
        role=create_user_body.role,
        age=create_user_body.age,
    )

    db.add(user)
    db.commit()


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):

    user = db.query(Users).filter(Users.username == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    if not bcrypt_context.verify(form_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    token = create_access_token(username=user.username, user_id=user.user_id, role=user.role, expires_delta=timedelta(hours=1))  # type: ignore

    return {"access_token": token, "token_type": "bearer"}
