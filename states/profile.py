from aiogram.fsm.state import StatesGroup, State


class ProfileState(StatesGroup):
    weight = State()  # вес
    height = State()  # рост
    age = State()  # возраст
    activity = State()  # уровень активности (минуты в день)
    gender = State()  # пол
    city = State()  # город
    calories_goal = State()  # калории цель
