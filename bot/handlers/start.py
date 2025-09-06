from aiogram import Router, types
from aiogram.filters import Command
from bot.db import connect

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    conn = await connect()
    user = await conn.fetchrow("SELECT id FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if not user:
        await message.answer(
            "🔒 Для начала общения с ботом, пожалуйста зарегистрируйтесь.\n"
            "Для этого используйте команду /register"
        )
        return

    await message.answer("Привет! Я — твой фитнес-ассистент. Готов продолжить?")