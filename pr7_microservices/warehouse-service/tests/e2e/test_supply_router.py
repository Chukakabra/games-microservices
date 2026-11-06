import uuid
import requests

BASE_URL = "http://127.0.0.1:8005"


def test_create_supply_success():
    data = {
        "game_id": str(uuid.uuid4()),
        "qty": 100,
        "supplier": "GameDistributor LLC"
    }
    r = requests.post(f"{BASE_URL}/supplies", json=data)
    assert r.status_code == 200
    body = r.json()
    assert body["qty"] == 100
    assert body["status"] == "EXPECTED"


def test_get_supply_not_found():
    r = requests.get(f"{BASE_URL}/supplies/{uuid.uuid4()}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Supply not found"


def test_receive_supply():
    data = {
        "game_id": str(uuid.uuid4()),
        "qty": 50,
        "supplier": "ООО ИгроТрейд"
    }
    created = requests.post(f"{BASE_URL}/supplies", json=data).json()
    supply_id = created["id"]

    r = requests.post(f"{BASE_URL}/supplies/{supply_id}/receive")
    assert r.status_code == 200
    assert r.json()["status"] == "RECEIVED"