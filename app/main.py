from fastapi import FastAPI
from pydantic import BaseModel
from app.database import engine
from app import models
from app.routers import auth, todos
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(todos.router)
app.include_router(auth.router)
@app.get("/")
async def root():
    return{"message":"Api is running"}

