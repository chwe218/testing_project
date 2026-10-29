import pytest
from fastapi.testclient import TestClient
from app.main import app,cart,games

client=TestClient(app)

@pytest.fixture(autouse=True)
def reset_cart():
    #每个测试开始前清空购物车
    cart.clear()
    yield
    #每个测试结束后再清空
    cart.clear()

def test_add_to_cart_success():
    response=client.post(
        "/cart",
        json={"game_id":1,"quantity":2}
    )

    assert response.status_code==200
    assert response.json()["quantity"]==2
    assert cart[1]==2


@pytest.mark.parametrize("quantity",[0,-1,6])
def test_invalid_quantity(quantity):
    response=client.post(
        "/cart",
        json={"game_id":1,"quantity":quantity}
    )
    assert response.status_code == 422
    assert cart == {}

def test_game_not_found():
    response = client.post(
        "/cart",
        json={"game_id": 999, "quantity": 2}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_insufficient_stock():
    original_stock=games[1]["stock"]
    try:
        games[1]["stock"]=3
        response = client.post(
            "/cart",
            json={"game_id": 1, "quantity": 4}
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Insufficient stock"
        assert cart == {}

    finally:
        games[1]["stock"] = original_stock


def test_cumulative_quantity_limit():
    first = client.post(
        "/cart",
        json={"game_id": 1, "quantity": 4}
    )

    second = client.post(
        "/cart",
        json={"game_id": 1, "quantity": 2}
    )

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Cart quantity limit exceeded"
    assert cart[1] == 4