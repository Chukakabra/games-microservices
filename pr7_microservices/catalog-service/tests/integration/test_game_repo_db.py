import uuid
import pytest
from app import models
from app.database import SessionLocal


@pytest.fixture()
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_create_game(db):
    game = models.Game(
        id=str(uuid.uuid4()),
        title="IntTest Game",
        genre="RPG",
        platform="PC",
        base_price=1990
    )
    db.add(game)
    db.commit()

    found = db.query(models.Game).filter_by(title="IntTest Game").first()
    assert found is not None
    assert found.base_price == 1990


def test_get_game_by_id(db):
    game_id = str(uuid.uuid4())
    game = models.Game(
        id=game_id, title="UniqueGame", genre="Action",
        platform="PS5", base_price=4990
    )
    db.add(game)
    db.commit()

    found = db.get(models.Game, game_id)
    assert found is not None
    assert found.title == "UniqueGame"