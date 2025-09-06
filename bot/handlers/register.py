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
        [InlineKeyboardButton(text="Да", callback_data="disability_yes")],
        [InlineKeyboardButton(text="Нет", callback_data="disability_no")],
        back_button("back_experience")
    ])
    await callback.message.answer("У вас есть инвалидность?", reply_markup=keyboard)
    await state.set_state(Registration.disability_status)
    await callback.answer()

@router.callback_query(F.data == "back_experience")
async def go_back_to_experience(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

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

@router.callback_query(F.data.startswith("disability_"))
async def process_disability(callback: CallbackQuery, state: FSMContext):
    if await is_registered_user(callback.from_user.id):
        await callback.answer("❗ Вы уже зарегистрированы.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except:
        pass

    has_disability = callback.data.split("_")[1] == "yes"
    await state.update_data(disability_status=has_disability)

    data = await state.get_data()

    conn = await connect()
    await conn.execute("""
        INSERT INTO users (id, name, age, sex, fitness_goal, height_cm, weight_kg, activity_level, experience_level, disability_status)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            age = EXCLUDED.age,
            sex = EXCLUDED.sex,
            fitness_goal = EXCLUDED.fitness_goal,
            height_cm = EXCLUDED.height_cm,
            weight_kg = EXCLUDED.weight_kg,
            activity_level = EXCLUDED.activity_level,
            experience_level = EXCLUDED.experience_level,
            disability_status = EXCLUDED.disability_status
    """,
        callback.from_user.id,
        callback.from_user.full_name,
        data["age"],
        data["sex"],
        data["fitness_goal"],
        data["height"],
        data["weight"],
        data["activity_level"],
        data["experience_level"],
        has_disability
    )
    await conn.close()

    await callback.message.answer("✅ Спасибо! Вы успешно зарегистрированы.")

    # Удалить inline-кнопки с предыдущего сообщения
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    await state.clear()
    await callback.answer()

@router.message(Command("reset"))
async def confirm_reset(message: types.Message):
    conn = await connect()
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", message.from_user.id)
    await conn.close()

    if not user or user["age"] is None or user["fitness_goal"] is None:
        await message.answer("🔒 Сначала завершите регистрацию.")
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Да, сбросить профиль")],
            [KeyboardButton(text="Нет, отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "⚠️ Вы уверены, что хотите сбросить ваш профиль? Это действие необратимо.",
        reply_markup=keyboard
    )

@router.message(F.text.in_(["Да, сбросить профиль", "Нет, отмена"]))
async def handle_reset_confirm(message: types.Message):
    if message.text == "Да, сбросить профиль":
        conn = await connect()
        await conn.execute("DELETE FROM users WHERE id = $1", message.from_user.id)
        await conn.close()
        await message.answer(
            "✅ Профиль успешно удалён. Вы можете начать заново с команды /register",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("❎ Сброс отменён.", reply_markup=ReplyKeyboardRemove())


