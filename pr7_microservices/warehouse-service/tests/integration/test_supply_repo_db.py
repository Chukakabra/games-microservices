import uuid
import pytest
from datetime import datetime
from app import models
from app.database import SessionLocal


@pytest.fixture()
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_create_supply(db):
    supply_id = str(uuid.uuid4())
    supply = models.Supply(
        id=supply_id,
        game_id=str(uuid.uuid4()),
        qty=100,
        supplier="GameDistributor LLC"
    )
    db.add(supply)
    db.commit()

    found = db.get(models.Supply, supply_id)
    assert found is not None
    assert found.qty == 100


def test_supply_defaults(db):
    supply = models.Supply(
        id=str(uuid.uuid4()),
        game_id=str(uuid.uuid4()),
        qty=50,
        supplier="ООО ИгроТрейд"
    )
    db.add(supply)
    db.commit()
    db.refresh(supply)

    assert supply.status == "EXPECTED"
    assert supply.received_at is None


def test_supply_receive_update(db):
    supply_id = str(uuid.uuid4())
    supply = models.Supply(
        id=supply_id,
        game_id=str(uuid.uuid4()),
        qty=200,
        supplier="GameDistributor LLC"
    )
    db.add(supply)
    db.commit()

    supply.status = "RECEIVED"
    supply.received_at = datetime.utcnow()
    db.commit()
    db.refresh(supply)

    assert supply.status == "RECEIVED"
    assert supply.received_at is not None