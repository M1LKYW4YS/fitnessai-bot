from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from bot.states.registration import Registration
from bot.db import connect

router = Router()


def back_button(callback_data: str):
    return [InlineKeyboardButton(text="⬅️ Назад", callback_data=callback_data)]

async def is_registered_user(user_id: int) -> bool:
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    await conn.close()
    return bool(user and user["age"] and user["fitness_goal"])

@router.message(Command("register"))
async def start_registration(message: types.Message, state: FSMContext):
    conn = await connect()
    existing_user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if existing_user and existing_user["age"] and existing_user["fitness_goal"]:
        await message.answer("Вы уже зарегистрированы ✅\nЧтобы начать заново, используйте /reset")
        return

    await message.answer("Введите ваш возраст:")
    await state.set_state(Registration.age)

@router.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await message.answer("Сначала завершите регистрацию или отправьте /cancel для отмены.")
        return

    try:
        age = int(message.text)
        if age < 10 or age > 100:
            raise ValueError
        await state.update_data(age=age)
    except ValueError:
        await message.answer("Введите корректный возраст (от 10 до 100).")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="sex_male")],
        [InlineKeyboardButton(text="Женский", callback_data="sex_female")],
        [InlineKeyboardButton(text="Другое", callback_data="sex_other")],
        back_button("back_age")
    ])
    await message.answer("Укажите ваш пол:", reply_markup=keyboard)
    await state.set_state(Registration.sex)

@router.callback_query(F.data == "back_age")
async def go_back_to_age(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    await state.set_state(Registration.age)
    await callback.message.answer("Введите ваш возраст:")
    await callback.answer()

@router.callback_query(F.data.startswith("sex_"))
async def process_sex(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    sex = callback.data.split("_")[1]
    await state.update_data(sex=sex)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Набор массы", callback_data="goal_gain")],
        [InlineKeyboardButton(text="⚖️ Похудение", callback_data="goal_lose")],
        [InlineKeyboardButton(text="🔄 Поддержание формы", callback_data="goal_maintain")],
        back_button("back_sex")
    ])
    await callback.message.answer("Какова ваша основная цель?", reply_markup=keyboard)
    await state.set_state(Registration.fitness_goal)
    await callback.answer()

@router.callback_query(F.data == "back_sex")
async def go_back_to_sex(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="sex_male")],
        [InlineKeyboardButton(text="Женский", callback_data="sex_female")],
        [InlineKeyboardButton(text="Другое", callback_data="sex_other")],
        back_button("back_age")
    ])
    await callback.message.answer("Укажите ваш пол:", reply_markup=keyboard)
    await state.set_state(Registration.sex)
    await callback.answer()

@router.callback_query(F.data.startswith("goal_"))
async def process_goal(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    mapping = {
        "gain": "Набор массы",
        "lose": "Похудение",
        "maintain": "Поддержание формы"
    }
    goal_key = callback.data.split("_")[1]
    await state.update_data(fitness_goal=mapping[goal_key])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        back_button("back_goal")
    ])
    sent_msg = await callback.message.answer("Введите ваш рост в см:", reply_markup=keyboard)

    # 💾 Сохраняем ID, чтобы потом удалить
    await state.update_data(last_bot_message_id=sent_msg.message_id)

    await state.set_state(Registration.height)
    await callback.answer()


@router.callback_query(F.data == "back_goal")
async def go_back_to_goal(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Набор массы", callback_data="goal_gain")],
        [InlineKeyboardButton(text="⚖️ Похудение", callback_data="goal_lose")],
        [InlineKeyboardButton(text="🔄 Поддержание формы", callback_data="goal_maintain")],
        back_button("back_sex")
    ])
    await callback.message.answer("Какова ваша основная цель?", reply_markup=keyboard)
    await state.set_state(Registration.fitness_goal)
    await callback.answer()

@router.message(Registration.height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if height < 100 or height > 250:
            raise ValueError
        await state.update_data(height=height)
    except ValueError:
        await message.answer("Введите корректный рост (от 100 до 250 см).")
        return

    # Удаляем предыдущее сообщение с кнопкой, если оно есть
    data = await state.get_data()
    old_msg_id = data.get("last_bot_message_id")
    if old_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=old_msg_id)
        except:
            pass

    # Отправляем новое сообщение и сохраняем его ID
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        back_button("back_height")
    ])
    sent_msg = await message.answer("Введите ваш вес в кг:", reply_markup=keyboard)
    await state.update_data(last_bot_message_id=sent_msg.message_id)

    await state.set_state(Registration.weight)

@router.callback_query(F.data == "back_height")
async def go_back_to_height(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer("Введите ваш рост в см:")
    await state.set_state(Registration.height)
    await callback.answer()

@router.message(Registration.weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight < 30 or weight > 300:
            raise ValueError
        await state.update_data(weight=weight)
    except ValueError:
        await message.answer("Введите корректный вес (от 30 до 300 кг).")
        return

    # Удаляем предыдущее сообщение с кнопкой, если оно есть
    data = await state.get_data()
    old_msg_id = data.get("last_bot_message_id")
    if old_msg_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=old_msg_id)
        except:
            pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Низкий", callback_data="activity_low")],
        [InlineKeyboardButton(text="Средний", callback_data="activity_medium")],
        [InlineKeyboardButton(text="Высокий", callback_data="activity_high")],
        back_button("back_weight")
    ])
    sent_msg = await message.answer("Укажите уровень вашей физической активности:", reply_markup=keyboard)
    await state.update_data(last_bot_message_id=sent_msg.message_id)

    await state.set_state(Registration.activity_level)

@router.callback_query(F.data == "back_weight")
async def go_back_to_weight(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        back_button("back_height")
    ])
    sent_msg = await callback.message.answer("Введите ваш вес в кг:", reply_markup=keyboard)

    await state.update_data(last_bot_message_id=sent_msg.message_id)
    await state.set_state(Registration.weight)
    await callback.answer()

@router.callback_query(F.data.startswith("activity_"))
async def process_activity(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    activity = callback.data.split("_")[1]
    await state.update_data(activity_level=activity)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новичок", callback_data="exp_beginner")],
        [InlineKeyboardButton(text="Средний", callback_data="exp_intermediate")],
        [InlineKeyboardButton(text="Продвинутый", callback_data="exp_advanced")],
        back_button("back_activity")
    ])
    await callback.message.answer("Укажите ваш уровень опыта:", reply_markup=keyboard)
    await state.set_state(Registration.experience_level)
    await callback.answer()

@router.callback_query(F.data == "back_activity")
async def go_back_to_activity(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Низкий", callback_data="activity_low")],
        [InlineKeyboardButton(text="Средний", callback_data="activity_medium")],
        [InlineKeyboardButton(text="Высокий", callback_data="activity_high")],
        back_button("back_weight")
    ])
    await callback.message.answer("Укажите уровень вашей физической активности:", reply_markup=keyboard)
    await state.set_state(Registration.activity_level)
    await callback.answer()

@router.callback_query(F.data.startswith("exp_"))
async def process_experience(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    experience = callback.data.split("_")[1]
    await state.update_data(experience_level=experience)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Нет", callback_data="injury_no")],
        [InlineKeyboardButton(text="Да", callback_data="injury_yes")],
        back_button("back_experience")
    ])
    await callback.message.answer("Есть ли у вас травмы, которые могут повлиять на тренировки?", reply_markup=keyboard)
    await state.set_state(Registration.injury_info)
    await callback.answer()


@router.callback_query(F.data == "back_experience")
async def go_back_to_experience(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новичок", callback_data="exp_beginner")],
        [InlineKeyboardButton(text="Средний", callback_data="exp_intermediate")],
        [InlineKeyboardButton(text="Продвинутый", callback_data="exp_advanced")],
        back_button("back_activity")
    ])
    await callback.message.answer("Укажите ваш уровень опыта:", reply_markup=keyboard)
    await state.set_state(Registration.experience_level)
    await callback.answer()


@router.callback_query(F.data.startswith("injury_"))
async def process_injury(callback: CallbackQuery, state: FSMContext):
    has_injury = callback.data.split("_")[1] == "yes"
    await state.update_data(has_injury=has_injury)

    try:
        await callback.message.delete()
    except:
        pass

    if has_injury:
        await callback.message.answer("Пожалуйста, уточните, какие у вас травмы:")
        await state.set_state(Registration.injury_details)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Нет", callback_data="health_no")],
            [InlineKeyboardButton(text="Да", callback_data="health_yes")],
            back_button("back_injury")
        ])
        await callback.message.answer("Есть ли у вас заболевания, которые могут повлиять на тренировки?", reply_markup=keyboard)
        await state.set_state(Registration.health_conditions)

    await callback.answer()


@router.message(Registration.injury_details)
async def process_injury_details(message: types.Message, state: FSMContext):
    await state.update_data(injury_info=message.text)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Нет", callback_data="health_no")],
        [InlineKeyboardButton(text="Да", callback_data="health_yes")],
        back_button("back_injury")
    ])
    await message.answer("Есть ли у вас заболевания, которые могут повлиять на тренировки?", reply_markup=keyboard)
    await state.set_state(Registration.health_conditions)


@router.callback_query(F.data == "back_injury")
async def go_back_to_injury(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Нет", callback_data="injury_no")],
        [InlineKeyboardButton(text="Да", callback_data="injury_yes")],
        back_button("back_experience")
    ])
    await callback.message.answer("Есть ли у вас травмы, которые могут повлиять на тренировки?", reply_markup=keyboard)
    await state.set_state(Registration.injury_info)
    await callback.answer()


@router.callback_query(F.data.startswith("health_"))
async def process_health(callback: CallbackQuery, state: FSMContext):
    has_health_issue = callback.data.split("_")[1] == "yes"
    await state.update_data(has_health_issue=has_health_issue)

    try:
        await callback.message.delete()
    except:
        pass

    if has_health_issue:
        await callback.message.answer("Пожалуйста, уточните, какие заболевания:")
        await state.set_state(Registration.health_details)
    else:
        await finalize_registration(callback, state)


@router.message(Registration.health_details)
async def process_health_details(message: types.Message, state: FSMContext):
    await state.update_data(health_conditions=message.text)
    await finalize_registration(message, state)


async def finalize_registration(event, state: FSMContext):
    """Финальное сохранение данных пользователя"""
    data = await state.get_data()

    conn = await connect()
    await conn.execute("""
        INSERT INTO users (id, name, age, sex, fitness_goal, height_cm, weight_kg,
                           activity_level, experience_level, injury_info, health_conditions)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            age = EXCLUDED.age,
            sex = EXCLUDED.sex,
            fitness_goal = EXCLUDED.fitness_goal,
            height_cm = EXCLUDED.height_cm,
            weight_kg = EXCLUDED.weight_kg,
            activity_level = EXCLUDED.activity_level,
            experience_level = EXCLUDED.experience_level,
            injury_info = EXCLUDED.injury_info,
            health_conditions = EXCLUDED.health_conditions
    """,
        event.from_user.id,
        event.from_user.full_name,
        data["age"],
        data["sex"],
        data["fitness_goal"],
        data["height"],
        data["weight"],
        data["activity_level"],
        data["experience_level"],
        data.get("injury_info", "нет"),
        data.get("health_conditions", "нет")
    )
    await conn.close()

    await event.message.answer("✅ Спасибо! Вы успешно зарегистрированы.")
    await state.clear()

