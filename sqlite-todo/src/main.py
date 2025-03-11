"""Main file"""

from fastapi import FastAPI
from starlette import status
from src.database import engine
from src import models
from router import auth, todos, admin, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Health check function

    Returns:
        string: Returns Healthy Server
    """

    return {"message": "Healthy Server!"}
