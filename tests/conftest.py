import pytest
from fastapi.testclient import TestClient
from app.main import app,cart,games
from app.database import get_connection

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


#在库存不足测试中把 Pixel Quest 的库存改成了 3，所以测试结束后必须恢复为 10。
@pytest.fixture(autouse=True)
def reset_data():
    with get_connection() as conn:
        conn.execute("DELETE FROM cart")
        conn.execute(
            "UPDATE games SET stock = 10 WHERE id = 1"
        )
        conn.execute(
            "UPDATE games SET stock = 5 WHERE id = 2"
        )
        conn.commit()

    yield

    with get_connection() as conn:
        conn.execute("DELETE FROM cart")
        conn.execute(
            "UPDATE games SET stock = 10 WHERE id = 1"
        )
        conn.execute(
            "UPDATE games SET stock = 5 WHERE id = 2"
        )
        conn.commit()