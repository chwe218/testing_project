
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pathlib import Path
from fastapi.responses import FileResponse

import os

#创建一个FastAPI应用，保存到app这个变量里
app = FastAPI()
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
    return list(games.values())

@app.get("/games/{game_id}")
def get_game(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id]

#定义添加购物车时接收的数据
class CartItem(BaseModel):
    game_id:int
    quantity:int=Field(ge=1,le=5)


@app.post("/cart")
def add_to_cart(item:CartItem):
    #检查游戏是否存在
    if item.game_id not in games:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )
    game=games[item.game_id]

   #计算购物车里面已有的数量 
    current_quantity=cart.get(item.game_id,0)
    new_quantity=current_quantity+item.quantity

    #检查累计购买数量限制
    if new_quantity>5:
        raise HTTPException(
            status_code=400,
            detail="Cart quantity cannot exceed 5"
        )
    
        
    #检查库存
    if new_quantity>game["stock"]:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    #添加到购物车
    cart[item.game_id] = new_quantity

    return {
        "message": "Added to cart successfully",
        "game_id": item.game_id,
        "quantity": new_quantity
    }


# 仅在测试环境启用的接口
if os.getenv("GAME_STORE_TESTING") == "1":

    @app.post("/test/reset", include_in_schema=False)
    def reset_test_data():
        cart.clear()

        return {
            "message": "Test data reset successfully"
        }
