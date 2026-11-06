import uuid
import pytest
from app import models
from app.database import SessionLocal


@pytest.fixture()
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_create_client(db):
    email = f"int_{uuid.uuid4().hex[:6]}@mail.com"
    client = models.Client(
        id=str(uuid.uuid4()),
        email=email,
        display_name="IntTest Client"
    )
    db.add(client)
    db.commit()

    found = db.query(models.Client).filter_by(email=email).first()
    assert found is not None
    assert found.display_name == "IntTest Client"


def test_client_defaults(db):
    email = f"def_{uuid.uuid4().hex[:6]}@mail.com"
    client = models.Client(
        id=str(uuid.uuid4()),
        email=email,
        display_name="Defaults Client"
    )
    db.add(client)
    db.commit()
    db.refresh(client)

    assert client.bonus_balance == 0
    assert client.status == "ACTIVE"


def test_client_unique_email(db):
    email = f"uniq_{uuid.uuid4().hex[:6]}@mail.com"
    c1 = models.Client(id=str(uuid.uuid4()), email=email, display_name="One")
    db.add(c1)
    db.commit()

    c2 = models.Client(id=str(uuid.uuid4()), email=email, display_name="Two")
    with pytest.raises(Exception):
        db.add(c2)
        db.commit()
    db.rollback()