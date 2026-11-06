import uuid
import requests

BASE_URL = "http://127.0.0.1:8006"


def test_create_review_success():
    data = {
        "client_id": str(uuid.uuid4()),
        "game_id": str(uuid.uuid4()),
        "text": "E2E отзыв",
        "rating": 5
    }
    r = requests.post(f"{BASE_URL}/reviews", json=data)
    assert r.status_code == 200
    body = r.json()
    assert body["rating"] == 5
    assert body["status"] == "PUBLISHED"


def test_create_review_invalid_rating():
    data = {
        "client_id": str(uuid.uuid4()),
        "game_id": str(uuid.uuid4()),
        "text": "Плохая оценка",
        "rating": 10
    }
    r = requests.post(f"{BASE_URL}/reviews", json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == "Rating must be between 1 and 5"


def test_update_rating():
    data = {
        "client_id": str(uuid.uuid4()),
        "game_id": str(uuid.uuid4()),
        "text": "Изменил мнение",
        "rating": 3
    }
    created = requests.post(f"{BASE_URL}/reviews", json=data).json()
    review_id = created["id"]

    r = requests.post(f"{BASE_URL}/reviews/{review_id}/rating", params={"rating": 5})
    assert r.status_code == 200
    assert r.json()["rating"] == 5