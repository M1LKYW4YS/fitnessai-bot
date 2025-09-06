from aiogram import Router, types
from aiogram.filters import Command
from bot.db import connect

router = Router()

@router.message(Command("profile"))
async def profile_cmd(message: types.Message):
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if user:
        # Отображение пола
        sex_display = {
            "male": "Мужской",
            "female": "Женский",
            "other": "Другое"
        }.get(user["sex"], "Не указано")

        # Отображение уровня активности
        activity_display = {
            "low": "Низкий",
            "medium": "Средний",
            "high": "Высокий"
        }.get(user["activity_level"], "Не указано")

        # Отображение уровня опыта
        experience_display = {
            "beginner": "Новичок",
            "intermediate": "Средний",
            "advanced": "Продвинутый"
        }.get(user["experience_level"], "Не указано")

        profile_info = (
            f"👤 Профиль пользователя:\n\n"
            f"Имя: {user['name'] or 'Не указано'}\n"
            f"Возраст: {user['age'] or 'Не указано'}\n"
            f"Пол: {sex_display}\n"
            f"Рост: {user['height_cm'] or 'Не указано'} см\n"
            f"Вес: {user['weight_kg'] or 'Не указано'} кг\n"
            f"Цель: {user['fitness_goal'] or 'Не указано'}\n"
            f"Уровень активности: {activity_display}\n"
            f"Опыт: {experience_display}\n"
            f"Инвалидность: {'Да' if user['disability_status'] else 'Нет'}\n"
            f"Дата регистрации: {user['created_at'].strftime('%d.%m.%Y %H:%M') if user['created_at'] else 'Не указано'}"
        )
        await message.answer(profile_info)
    else:
        await message.answer("Пользователь не найден. Напишите /register для начала.")