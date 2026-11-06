import uuid
import requests

BASE_URL = "http://127.0.0.1:8004"


def test_create_delivery_success():
    data = {
        "order_id": str(uuid.uuid4()),
        "courier_id": str(uuid.uuid4()),
        "address": "г. Москва, пр. Вернадского, 78"
    }
    r = requests.post(f"{BASE_URL}/deliveries", json=data)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "COURIER_ASSIGNED"
    assert "id" in body


def test_get_delivery_not_found():
    r = requests.get(f"{BASE_URL}/deliveries/{uuid.uuid4()}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Delivery not found"


def test_complete_delivery():
    data = {
        "order_id": str(uuid.uuid4()),
        "courier_id": str(uuid.uuid4()),
        "address": "г. Москва"
    }
    created = requests.post(f"{BASE_URL}/deliveries", json=data).json()
    delivery_id = created["id"]

    r = requests.post(f"{BASE_URL}/deliveries/{delivery_id}/complete")
    assert r.status_code == 200
    assert r.json()["status"] == "DELIVERED"