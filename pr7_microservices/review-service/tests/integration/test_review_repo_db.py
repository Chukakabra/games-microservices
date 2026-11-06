import uuid
import pytest
from app import models
from app.database import SessionLocal


@pytest.fixture()
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_create_review(db):
    review_id = str(uuid.uuid4())
    review = models.Review(
        id=review_id,
        client_id=str(uuid.uuid4()),
        game_id=str(uuid.uuid4()),
        text="Отличная игра!",
        rating=5
    )
    db.add(review)
    db.commit()

    found = db.get(models.Review, review_id)
    assert found is not None
    assert found.rating == 5
    assert found.text == "Отличная игра!"


def test_review_defaults(db):
    review = models.Review(
        id=str(uuid.uuid4()),
        client_id=str(uuid.uuid4()),
        game_id=str(uuid.uuid4()),
        text="Норм",
        rating=4
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    assert review.status == "PUBLISHED"
    assert review.created_at is not None


def test_review_rating_update(db):
    review_id = str(uuid.uuid4())
    review = models.Review(
        id=review_id,
        client_id=str(uuid.uuid4()),
        game_id=str(uuid.uuid4()),
        text="Сначала понравилось",
        rating=3
    )
    db.add(review)
    db.commit()

    review.rating = 5
    db.commit()
    db.refresh(review)

    assert review.rating == 5