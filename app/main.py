
from fastapi import FastAPI, HTTPException

app = FastAPI()

games = {
    1: {"id": 1, "name": "Pixel Quest", "price": 49, "stock": 10},
    2: {"id": 2, "name": "Moon Farm", "price": 79, "stock": 5}
}

@app.get("/games")
def get_games():
    return list(games.values())

@app.get("/games/{game_id}")
def get_game(game_id: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id]
