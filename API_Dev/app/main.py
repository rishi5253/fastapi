from fastapi import FastAPI
from . import model
from .database import engine
from app.routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins =["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,#
    allow_methods=["*"],#allow what kind of request you want to allowed (post,get,put,delete)
    allow_headers=["*"],
)



model.Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(post.router)

app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def home():
    return {
        "message": "FastAPI application is running successfully!",
        "status": "Healthy"
    }