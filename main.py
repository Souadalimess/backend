from typing import List
from uuid import uuid4
from fastapi import FastAPI

from models import Hero

app = FastAPI()

db: List[Hero] = [
    Hero(
        id=uuid4(), name="Souad"
    )
]


@app.get("/")
async def root():
    return {"Init": "First API with FastAPI!"}


@app.get("/api/v1/heroes")
async def fetch_heroes():
    return db
