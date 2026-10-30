
import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_get_all_games(client):
    response = client.get("/games")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.parametrize("game_id", [1, 2])
def test_get_game(game_id,client):
    response = client.get(f"/games/{game_id}")

    assert response.status_code == 200
    assert response.json()["id"] == game_id
    assert response.json()["price"] >= 0


def test_game_not_found(client):
    response = client.get("/games/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"

def test_invalid_game_id(client):
    response=client.get("/games/abc")
    assert response.status_code==422

def test_negative_game_id(client):
    response=client.get("/game/-1")
    assert response.status_code==404

def test_zero_game_id(client):
    response=client.get("/game/0")
    assert response.status_code==404