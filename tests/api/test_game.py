
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_all_games():
    response = client.get("/games")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.parametrize("game_id", [1, 2])
def test_get_game(game_id):
    response = client.get(f"/games/{game_id}")

    assert response.status_code == 200
    assert response.json()["id"] == game_id
    assert response.json()["price"] >= 0


def test_game_not_found():
    response = client.get("/games/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"
