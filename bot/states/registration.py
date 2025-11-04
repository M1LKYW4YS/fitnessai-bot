from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    age = State()
    sex = State()
    fitness_goal = State()
    height = State()
    weight = State()
    activity_level = State()
    experience_level = State()
    has_injury = State()  # Есть ли травмы?
    injury_details = State()  # Уточнение травм
    has_health_condition = State()  # Есть ли заболевания?
    health_details = State()
