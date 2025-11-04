from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from bot.db import connect

router = Router()

# Обработка команды /reset
@router.message(Command("reset"))
async def confirm_reset(message: types.Message):
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if not user:
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
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", callback.from_user.id)

    if not user:
        await callback.message.answer("Пользователь не найден. Напишите /register для начала.")
        await conn.close()
        await callback.answer()
        return

    await conn.execute(
        """
        UPDATE users
        SET 
            age = NULL,
            sex = NULL,
            fitness_goal = NULL,
            height_cm = NULL,
            weight_kg = NULL,
            activity_level = NULL,
            experience_level = NULL,
            injury_info = NULL,
            health_conditions = NULL
        WHERE id = $1
        """,
        callback.from_user.id
    )
    await conn.close()

    await callback.message.answer("🗑 Ваш профиль был успешно сброшен.")
    await callback.answer()

# Пользователь отменил сброс
@router.callback_query(F.data == "reset_no")
async def cancel_reset(callback: CallbackQuery):
    await callback.message.answer("✅ Сброс отменён.")
    await callback.answer()