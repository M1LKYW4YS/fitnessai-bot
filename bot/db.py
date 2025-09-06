import asyncpg
from bot.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

async def connect():
    return await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

async def get_or_create_user(conn, telegram_id: int, name: str = None):
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", telegram_id)
    if not user:
        await conn.execute(
            "INSERT INTO users (id, name) VALUES ($1, $2)",
            telegram_id, name
        )
        return {"status": "created"}
    return {"status": "exists"}