from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service")


class GameCreate(BaseModel):
    title: str
    genre: str
    platform: str
    base_price: int


class GameResponse(BaseModel):
    id: str
    title: str
    genre: str
    platform: str
    base_price: int
    status: str


@app.post("/games", response_model=GameResponse)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    db_game = models.Game(
        id=str(uuid.uuid4()),
        title=game.title,
        genre=game.genre,
        platform=game.platform,
        base_price=game.base_price
    )
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return GameResponse(
        id=db_game.id, title=db_game.title, genre=db_game.genre,
        platform=db_game.platform, base_price=db_game.base_price, status=db_game.status
    )


@app.get("/games", response_model=list[GameResponse])
def list_games(genre: Optional[str] = None, platform: Optional[str] = None,
               db: Session = Depends(get_db)):
    query = db.query(models.Game)
    if genre:
        query = query.filter(models.Game.genre == genre)
    if platform:
        query = query.filter(models.Game.platform == platform)
    return [
        GameResponse(id=g.id, title=g.title, genre=g.genre,
                     platform=g.platform, base_price=g.base_price, status=g.status)
        for g in query.all()
    ]


@app.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameResponse(
        id=game.id, title=game.title, genre=game.genre,
        platform=game.platform, base_price=game.base_price, status=game.status
    )


@app.put("/games/{game_id}/price", response_model=GameResponse)
def change_price(game_id: str, new_price: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game.base_price = new_price
    db.commit()
    db.refresh(game)
    return GameResponse(
        id=game.id, title=game.title, genre=game.genre,
        platform=game.platform, base_price=game.base_price, status=game.status
    )