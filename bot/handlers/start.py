from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.db import connect
from openai import OpenAI
import os

router = Router()

# Инициализация клиента OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if not user:
        await message.answer(
            "🔒 Для начала общения с ботом, пожалуйста зарегистрируйтесь.\n"
            "Для этого используйте команду /register"
        )
        return

    await message.answer(
        f"Привет, {user['name']}! 👋\n"
        "Я — твой персональный фитнес-ассистент.\n"
        "Можешь спросить меня о питании, тренировках, сне или мотивации 💪"
    )


# Обработчик всех текстовых сообщений (кроме команд)
@router.message(F.text)
async def chat_with_ai(message: types.Message, state: FSMContext):
    # Проверяем, есть ли активное состояние FSM
    user_state = await state.get_state()
    if user_state is not None:
        # Если пользователь находится в процессе регистрации или другой FSM — ничего не делаем
        return

    # Игнорируем команды
    if message.text.startswith("/"):
        return

    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if not user:
        await message.answer("⚠️ Пожалуйста, сначала пройдите регистрацию с помощью команды /register.")
        return

    # Формируем персональный промт
    system_prompt = f"""
Ты — персональный фитнес-тренер и наставник.
Вот данные пользователя:
- Имя: {user['name']}
- Возраст: {user['age']}
- Пол: {user['sex']}
- Цель: {user['fitness_goal']}
- Рост: {user['height_cm']} см
- Вес: {user['weight_kg']} кг
- Активность: {user['activity_level']}
- Опыт тренировок: {user['experience_level']}
- Инвалидность: {"есть" if user['disability_status'] else "нет"}

🎯 Твоя задача — помогать пользователю достигать его фитнес-целей:
- давать советы по питанию, тренировкам и восстановлению;
- мотивировать без давления;
- объяснять просто, как будто общаешься с другом;
- если пользователь спрашивает что-то вне фитнеса — мягко возвращай разговор к теме здоровья и спорта.

🗣 Стиль общения:
- дружелюбный, уверенный, без занудства;
- ответы максимум 2–4 предложения;
- не используй сложные научные термины;
- без «по моим данным» и без упоминаний ChatGPT, ИИ или OpenAI.

Если пользователь пишет что-то вроде «что мне делать сегодня», «как быть», «я устал» —
ответь как тренер, поддержи и предложи конкретный шаг.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.text},
            ]
        )

        answer = response.choices[0].message.content
        await message.answer(answer)

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка при обращении к ИИ. Попробуйте позже.")
        print("Ошибка OpenAI:", e)