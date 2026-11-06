import uuid
import requests
import pytest

CLIENT_URL = "http://127.0.0.1:8002"
PAYMENT_URL = "http://127.0.0.1:8003"


@pytest.fixture()
def created_client():
    client = {
        "email": f"e2e_{uuid.uuid4().hex[:6]}@mail.com",
        "display_name": "E2E Client"
    }
    r = requests.post(f"{CLIENT_URL}/clients", json=client)
    assert r.status_code == 200
    return r.json()


def test_create_payment_success(created_client):
    data = {
        "order_id": str(uuid.uuid4()),
        "client_id": created_client["id"],
        "amount": 3990
    }
    r = requests.post(f"{PAYMENT_URL}/payments", json=data)
    assert r.status_code == 200
    body = r.json()
    # Вложенный вызов: PaymentService проверил клиента в ClientService
    assert body["status"] == "PENDING"
    assert body["amount"] == 3990


def test_create_payment_client_not_found():
    data = {
        "order_id": str(uuid.uuid4()),
        "client_id": str(uuid.uuid4()),  # несуществующий клиент
        "amount": 3990
    }
    r = requests.post(f"{PAYMENT_URL}/payments", json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == "Client not found"


def test_pay_payment(created_client):
    data = {
        "order_id": str(uuid.uuid4()),
        "client_id": created_client["id"],
        "amount": 3990
    }
    created = requests.post(f"{PAYMENT_URL}/payments", json=data).json()
    payment_id = created["id"]

    r = requests.post(f"{PAYMENT_URL}/payments/{payment_id}/pay")
    assert r.status_code == 200
    assert r.json()["status"] == "PAID"