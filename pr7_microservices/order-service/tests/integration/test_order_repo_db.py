import uuid
import pytest
from app import models
from app.database import SessionLocal


@pytest.fixture()
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_create_order(db):
    order_id = str(uuid.uuid4())
    order = models.Order(
        id=order_id,
        client_id="client-int-1",
        game_id=str(uuid.uuid4()),
        delivery_address="г. Москва, пр. Вернадского, 78",
        total=3990
    )
    db.add(order)
    db.commit()

    found = db.get(models.Order, order_id)
    assert found is not None
    assert found.total == 3990
    assert found.status == "CREATED"