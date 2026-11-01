import pytest
from fastapi.testclient import TestClient
from app.main import app,cart,games
from app.database import get_connection



def test_add_to_cart_success(client):
    response = client.post(
        "/cart",
        json={"game_id": 1, "quantity": 2}
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 2

     # 查询 SQLite，验证购物车数据

    with get_connection() as conn:
        row = conn.execute(
        "SELECT quantity FROM cart WHERE game_id = ?",
        (1,)
    ).fetchone()

    assert row is not None
    assert row["quantity"] == 2


@pytest.mark.parametrize("quantity",[0,-1,6])
def test_invalid_quantity(quantity,client):
    response=client.post(
        "/cart",
        json={"game_id":1,"quantity":quantity}
    )
    assert response.status_code == 422
    # 非法输入不应该写入数据库
    with get_connection() as conn:
        row = conn.execute(
            "SELECT quantity FROM cart WHERE game_id = ?",
            (1,)
        ).fetchone()

    assert row is None

def test_game_not_found(client):
    response = client.post(
        "/cart",
        json={"game_id": 999, "quantity": 2}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"

    # 不存在的游戏不应该进入购物车
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM cart WHERE game_id = ?",
            (999,)
        ).fetchone()

    assert row is None

def test_insufficient_stock(client):
    # 临时修改数据库中的库存
    with get_connection() as conn:
        conn.execute(
            "UPDATE games SET stock = ? WHERE id = ?",
            (3, 1)
        )
        conn.commit()

    # 库存只有3，尝试购买4
    response = client.post(
        "/cart",
        json={"game_id": 1, "quantity": 4}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough stock"

    # 库存不足不能产生购物车记录
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM cart WHERE game_id = ?",
            (1,)
        ).fetchone()

    assert row is None



def test_cumulative_quantity_limit(client):
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
    assert second.json()["detail"] == "Cart quantity cannot exceed 5"
    # 第二次失败后，数据库应保持原来的4份
    with get_connection() as conn:
        row = conn.execute(
            "SELECT quantity FROM cart WHERE game_id = ?",
            (1,)
        ).fetchone()

    assert row is not None
    assert row["quantity"] == 4