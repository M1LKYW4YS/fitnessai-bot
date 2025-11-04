from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from bot.db import connect

router = Router()

# Проверка регистрации
async def is_registered(user_id: int) -> bool:
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    await conn.close()
    return bool(user and user["age"] and user["fitness_goal"])


# Обработка команды /reset
@router.message(Command("reset"))
async def confirm_reset(message: types.Message):
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if not user or user["age"] is None or user["fitness_goal"] is None:
        await message.answer("Пользователь не найден. Напишите /register для начала.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, сбросить", callback_data="reset_yes")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="reset_no")]
    ])
    await message.answer(
        "Вы уверены, что хотите сбросить профиль? Это действие необратимо.",
        reply_markup=keyboard
    )


# Пользователь подтвердил сброс
@router.callback_query(F.data == "reset_yes")
async def process_reset(callback: CallbackQuery):
    user_id = callback.from_user.id
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)

    if not user:
        await callback.message.edit_text("Пользователь не найден. Напишите /register для начала.")
        await callback.answer()
        await conn.close()
        return

    # 🗑 Полное удаление профиля
    await conn.execute("DELETE FROM users WHERE id = $1", user_id)
    await conn.close()

    await callback.message.edit_text("🗑️ Ваш профиль был успешно сброшен.")
    await callback.answer()


# Пользователь отменил сброс
@router.callback_query(F.data == "reset_no")
async def cancel_reset(callback: CallbackQuery):
    await callback.message.edit_text("✅ Сброс отменён.")
    await callback.answer()