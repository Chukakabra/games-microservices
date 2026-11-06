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


def test_create_delivery(db):
    delivery_id = str(uuid.uuid4())
    delivery = models.Delivery(
        id=delivery_id,
        order_id=str(uuid.uuid4()),
        courier_id=str(uuid.uuid4()),
        address="г. Москва, пр. Вернадского, 78"
    )
    db.add(delivery)
    db.commit()

    found = db.get(models.Delivery, delivery_id)
    assert found is not None
    assert found.address == "г. Москва, пр. Вернадского, 78"


def test_delivery_defaults(db):
    delivery = models.Delivery(
        id=str(uuid.uuid4()),
        order_id=str(uuid.uuid4()),
        courier_id=str(uuid.uuid4()),
        address="г. Москва"
    )
    db.add(delivery)
    db.commit()
    db.refresh(delivery)

    assert delivery.status == "COURIER_ASSIGNED"
    assert delivery.delivered_at is None


def test_delivery_status_update(db):
    delivery_id = str(uuid.uuid4())
    delivery = models.Delivery(
        id=delivery_id,
        order_id=str(uuid.uuid4()),
        courier_id=str(uuid.uuid4()),
        address="г. Москва"
    )
    db.add(delivery)
    db.commit()

    delivery.status = "DELIVERED"
    delivery.delivered_at = datetime.utcnow()
    db.commit()
    db.refresh(delivery)

    assert delivery.status == "DELIVERED"
    assert delivery.delivered_at is not None