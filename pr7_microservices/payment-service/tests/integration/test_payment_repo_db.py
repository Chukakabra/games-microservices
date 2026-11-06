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


def test_create_payment(db):
    payment_id = str(uuid.uuid4())
    payment = models.Payment(
        id=payment_id,
        order_id=str(uuid.uuid4()),
        client_id=str(uuid.uuid4()),
        amount=3990
    )
    db.add(payment)
    db.commit()

    found = db.get(models.Payment, payment_id)
    assert found is not None
    assert found.amount == 3990


def test_payment_defaults(db):
    payment = models.Payment(
        id=str(uuid.uuid4()),
        order_id=str(uuid.uuid4()),
        client_id=str(uuid.uuid4()),
        amount=1990
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    assert payment.status == "PENDING"
    assert payment.paid_at is None


def test_payment_status_update(db):
    payment_id = str(uuid.uuid4())
    payment = models.Payment(
        id=payment_id,
        order_id=str(uuid.uuid4()),
        client_id=str(uuid.uuid4()),
        amount=3990
    )
    db.add(payment)
    db.commit()

    payment.status = "PAID"
    payment.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)

    assert payment.status == "PAID"
    assert payment.paid_at is not None