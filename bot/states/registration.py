from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    age = State()
    sex = State()
    fitness_goal = State()
    height = State()
    weight = State()
    activity_level = State()
    experience_level = State()
    disability_status = State()
