import uuid
import requests
import pytest

CATALOG_URL = "http://127.0.0.1:8000"
ORDER_URL = "http://127.0.0.1:8001"


@pytest.fixture()
def created_game():
    game = {
        "title": f"E2E_{uuid.uuid4().hex[:6]}",
        "genre": "RPG",
        "platform": "PC",
        "base_price": 3990
    }
    r = requests.post(f"{CATALOG_URL}/games", json=game)
    assert r.status_code == 200
    return r.json()


def test_create_order_success(created_game):
    data = {
        "client_id": "client-e2e-1",
        "game_id": created_game["id"],
        "delivery_address": "г. Москва, пр. Вернадского, 78"
    }
    r = requests.post(f"{ORDER_URL}/orders", json=data)
    assert r.status_code == 200
    body = r.json()
    # Вложенный вызов: total взят из CatalogService
    assert body["total"] == created_game["base_price"]
    assert body["status"] == "CREATED"


def test_create_order_game_not_found():
    data = {
        "client_id": "client-e2e-1",
        "game_id": str(uuid.uuid4()),  # несуществующая игра
        "delivery_address": "г. Москва"
    }
    r = requests.post(f"{ORDER_URL}/orders", json=data)
    assert r.status_code == 400
    assert r.json()["detail"] == "Game not found in catalog"


def test_cancel_order(created_game):
    data = {
        "client_id": "client-e2e-1",
        "game_id": created_game["id"],
        "delivery_address": "г. Москва"
    }
    created = requests.post(f"{ORDER_URL}/orders", json=data).json()
    order_id = created["id"]

    r = requests.post(f"{ORDER_URL}/orders/{order_id}/cancel")
    assert r.status_code == 200
    assert r.json()["status"] == "CANCELLED"