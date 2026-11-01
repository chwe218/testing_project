
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pathlib import Path
from fastapi.responses import FileResponse

from app.database import get_connection, init_db

import os

#创建一个FastAPI应用，保存到app这个变量里
app = FastAPI()
init_db()
BASE_DIR=Path(__file__).resolve().parent.parent

@app.get("/",include_in_schema=False)
def home():
    return FileResponse(BASE_DIR/"static"/"index.html")

games = {
    1: {"id": 1, "name": "Pixel Quest", "price": 49, "stock": 10},
    2: {"id": 2, "name": "Moon Farm", "price": 79, "stock": 5}
}

cart={}

@app.get("/games")
def get_games():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, price, stock FROM games ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]

@app.get("/games/{game_id}")
def get_game(game_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, price, stock FROM games WHERE id = ?",
            (game_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Game not found"
            )

        return dict(row)

#定义添加购物车时接收的数据
class CartItem(BaseModel):
    game_id:int
    quantity:int=Field(ge=1,le=5)


@app.post("/cart")
def add_to_cart(item:CartItem):
    
    with get_connection() as conn:
        #1.检查游戏是否存在    
        game=conn.execute("SELECT id,stock FROM games WHERE id= ?",
                          (item.game_id,)).fetchone()

        if game is None:
            raise HTTPException(
                        status_code=404,
                        detail="Game not found"
                    )
        
        #2.查询游戏目前在购物车中的数量
        row = conn.execute(
            "SELECT quantity FROM cart WHERE game_id = ?",
            (item.game_id,)
        ).fetchone()

        current_quantity = row["quantity"] if row else 0
        # 3. 计算新的累计数量
        new_quantity = current_quantity + item.quantity

        # 4. 检查库存
        if new_quantity > game["stock"]:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )

        # 5. 检查购物车累计数量限制
        if new_quantity > 5:
            raise HTTPException(
                status_code=400,
                detail="Cart quantity cannot exceed 5"
            )

        # 6. 更新或插入购物车记录
        conn.execute(
            """
            INSERT INTO cart (game_id, quantity)
            VALUES (?, ?)
            ON CONFLICT(game_id)
            DO UPDATE SET quantity = excluded.quantity
            """,
            (item.game_id, new_quantity)
        )

        conn.commit()

        return {
            "message": "Added to cart",
            "game_id": item.game_id,
            "quantity": new_quantity
            
        }




# 仅在测试环境启用的接口
if os.getenv("GAME_STORE_TESTING") == "1":

    @app.post("/test/reset", include_in_schema=False)
    def reset_test_data():
        with get_connection() as conn:
            conn.execute("DELETE FROM cart")
            conn.commit()

        return {
            "message": "Test data reset successfully"
        }
