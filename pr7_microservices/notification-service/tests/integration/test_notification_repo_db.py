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


def test_create_notification(db):
    notif_id = str(uuid.uuid4())
    notif = models.Notification(
        id=notif_id,
        client_id=str(uuid.uuid4()),
        channel="sms",
        text="Ваш заказ оплачен"
    )
    db.add(notif)
    db.commit()

    found = db.get(models.Notification, notif_id)
    assert found is not None
    assert found.channel == "sms"


def test_notification_defaults(db):
    notif = models.Notification(
        id=str(uuid.uuid4()),
        client_id=str(uuid.uuid4()),
        channel="email",
        text="Приветственное письмо"
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    assert notif.status == "PENDING"
    assert notif.sent_at is None


def test_notification_sent_update(db):
    notif_id = str(uuid.uuid4())
    notif = models.Notification(
        id=notif_id,
        client_id=str(uuid.uuid4()),
        channel="push",
        text="Анонс коллекционного издания"
    )
    db.add(notif)
    db.commit()

    notif.status = "SENT"
    notif.sent_at = datetime.utcnow()
    db.commit()
    db.refresh(notif)

    assert notif.status == "SENT"
    assert notif.sent_at is not None