from fastapi import FastAPI
from .import models
from .database import engine
from .routers import login, register, users

app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(login.router)
app.include_router(register.router)
app.include_router(users.router)


