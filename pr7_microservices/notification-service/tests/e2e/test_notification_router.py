import uuid
import requests

BASE_URL = "http://127.0.0.1:8007"


def test_create_notification_success():
    data = {
        "client_id": str(uuid.uuid4()),
        "channel": "sms",
        "text": "Ваш заказ оплачен"
    }
    r = requests.post(f"{BASE_URL}/notifications", json=data)
    assert r.status_code == 200
    body = r.json()
    assert body["channel"] == "sms"
    assert body["status"] == "PENDING"


def test_create_notification_invalid_channel():
    data = {
        "client_id": str(uuid.uuid4()),
        "channel": "telegram",
        "text": "Тест"
    }
    r = requests.post(f"{BASE_URL}/notifications", json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == "Channel must be sms, email or push"


def test_mark_notification_sent():
    data = {
        "client_id": str(uuid.uuid4()),
        "channel": "email",
        "text": "Чек по заказу"
    }
    created = requests.post(f"{BASE_URL}/notifications", json=data).json()
    notif_id = created["id"]

    r = requests.post(f"{BASE_URL}/notifications/{notif_id}/mark-sent")
    assert r.status_code == 200
    assert r.json()["status"] == "SENT"