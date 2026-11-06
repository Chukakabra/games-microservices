import uuid
import requests
import pytest

BASE_URL = "http://127.0.0.1:8002"


@pytest.fixture()
def client_data():
    return {
        "email": f"e2e_{uuid.uuid4().hex[:6]}@mail.com",
        "display_name": "E2E Client"
    }


def test_create_client_success(client_data):
    r = requests.post(f"{BASE_URL}/clients", json=client_data)
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == client_data["email"]
    assert "id" in body


def test_create_client_duplicate_email(client_data):
    requests.post(f"{BASE_URL}/clients", json=client_data)
    r = requests.post(f"{BASE_URL}/clients", json=client_data)
    assert r.status_code == 400
    assert r.json()["detail"] == "Email already registered"


def test_get_client_not_found():
    r = requests.get(f"{BASE_URL}/clients/{uuid.uuid4()}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Client not found"


def test_add_bonus(client_data):
    created = requests.post(f"{BASE_URL}/clients", json=client_data).json()
    client_id = created["id"]

    r = requests.post(f"{BASE_URL}/clients/{client_id}/bonus", params={"amount": 100})
    assert r.status_code == 200
    assert r.json()["bonus_balance"] == 100