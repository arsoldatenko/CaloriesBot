from aiogram.fsm.state import StatesGroup, State


class WaterState(StatesGroup):
    log_water = State()  # режим логирования воды
