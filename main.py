from fastapi import FastAPI, Depends, HTTPException

from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://frontend:4200",
    "http://localhost:4200/detail/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Hero(BaseModel):
    name: str


HEROES = []


@app.get("/heroes")
async def root(db: Session = Depends(get_db)):
    return db.query(models.Heroes).all()


@app.get("/heroes/{hero_id}")
def get_hero_by_id(hero_id: int, db: Session = Depends(get_db)):

    return db.query(models.Heroes).filter(models.Heroes.id == hero_id).first()


@app.post("/heroes")
async def create_hero(hero: Hero, db: Session = Depends(get_db)):

    hero_model = models.Heroes()
    hero_model.name = hero.name

    db.add(hero_model)
    db.commit()

    return hero


@app.put("/heroes/{hero_id}")
async def edit_hero(hero_id: int, hero: Hero, db: Session = Depends(get_db)):

    hero_model = db.query(models.Heroes).filter(
        models.Heroes.id == hero_id).first()

    if hero_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {hero_id}: This Hero don't exist"
        )
    hero_model.name = hero.name

    db.add(hero_model)
    db.commit()

    return hero


@app.delete("/heroes/{hero_id}")
async def delete_hero(hero_id: int, db: Session = Depends(get_db)):
    hero_model = db.query(models.Heroes).filter(
        models.Heroes.id == hero_id).first()

    if hero_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {hero_id}: This Hero don't exist"
        )

    db.query(models.Heroes).filter(models.Heroes.id == hero_id).delete()

    db.commit()
