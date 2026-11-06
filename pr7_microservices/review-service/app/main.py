from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from .database import Base, engine, get_db
from . import models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Review Service")

class ReviewCreate(BaseModel):
    client_id: str
    game_id: str
    text: str
    rating: int

class ReviewResponse(BaseModel):
    id: str
    client_id: str
    game_id: str
    text: str
    rating: int
    status: str

@app.post("/reviews", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    db_review = models.Review(
        id=str(uuid.uuid4()),
        client_id=review.client_id,
        game_id=review.game_id,
        text=review.text,
        rating=review.rating
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return ReviewResponse(
        id=db_review.id, client_id=db_review.client_id, game_id=db_review.game_id,
        text=db_review.text, rating=db_review.rating, status=db_review.status
    )

@app.post("/reviews/{review_id}/rating", response_model=ReviewResponse)
def update_rating(review_id: str, rating: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    review.rating = rating
    db.commit()
    db.refresh(review)
    return ReviewResponse(
        id=review.id, client_id=review.client_id, game_id=review.game_id,
        text=review.text, rating=review.rating, status=review.status
    )

@app.get("/reviews/{review_id}", response_model=ReviewResponse)
def get_review(review_id: str, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewResponse(
        id=review.id, client_id=review.client_id, game_id=review.game_id,
        text=review.text, rating=review.rating, status=review.status
    )

@app.get("/reviews", response_model=list[ReviewResponse])
def list_reviews(game_id: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Review)
    if game_id:
        query = query.filter(models.Review.game_id == game_id)
    return [
        ReviewResponse(id=r.id, client_id=r.client_id, game_id=r.game_id,
                       text=r.text, rating=r.rating, status=r.status)
        for r in query.all()
    ]