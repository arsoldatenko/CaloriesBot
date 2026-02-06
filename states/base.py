from aiogram.fsm.state import StatesGroup, State


class BaseState(StatesGroup):
    base = State()
