import uuid
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture()
def game_data():
    return {
        "title": f"E2E_{uuid.uuid4().hex[:6]}",
        "genre": "RPG",
        "platform": "PC",
        "base_price": 3990
    }


def test_create_game_success(game_data):
    r = requests.post(f"{BASE_URL}/games", json=game_data)
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == game_data["title"]
    assert "id" in body


def test_get_game_not_found():
    random_id = uuid.uuid4()
    r = requests.get(f"{BASE_URL}/games/{random_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Game not found"


def test_change_price(game_data):
    created = requests.post(f"{BASE_URL}/games", json=game_data).json()
    game_id = created["id"]

    r = requests.put(f"{BASE_URL}/games/{game_id}/price", params={"new_price": 2990})
    assert r.status_code == 200
    assert r.json()["base_price"] == 2990