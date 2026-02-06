from aiogram.fsm.state import StatesGroup, State


class WorkoutState(StatesGroup):
    log_workout = State()  # режим логирования воды
