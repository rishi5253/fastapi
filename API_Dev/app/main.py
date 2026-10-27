from fastapi import FastAPI
from . import model
from .database import engine
from app.routers import post,user,auth,vote


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(post.router)

app.include_router(auth.router)
app.include_router(vote.router)
