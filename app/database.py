import sqlite3
from pathlib import Path

#项目根目录
BASE_DIR=Path(__file__).resolve().parent.parent
#数据库文件位置
DB_PATH=BASE_DIR / "game_store.db"


def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:

        #创建游戏表
        conn.execute("""
        CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                stock INTEGER NOT NULL)
        """)

        # 创建购物车表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                game_id INTEGER PRIMARY KEY,
                quantity INTEGER NOT NULL,
                FOREIGN KEY (game_id)
                    REFERENCES games(id)
            )
        """)



        # 初始化游戏数据
        conn.executemany("""
            INSERT OR IGNORE INTO games
                (id, name, price, stock)
            VALUES (?, ?, ?, ?)
        """, [
            (1, "Pixel Quest", 49, 10),
            (2, "Moon Farm", 79, 5)
        ])

        conn.commit()

if __name__=="__main__":
    init_db()
    print(f"Database initialized: {DB_PATH}")