import pytest
from fastapi.testclient import TestClient
from app.main import app,cart,games

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def reset_data():
    original_games={
        game_id:game.copy()
        for game_id, game in games.items()
    }

    cart.clear()

    yield

    cart.clear()
    games.clear()
    games.update(original_games)
