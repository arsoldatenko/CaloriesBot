from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.workout import WorkoutState

router = Router()


@router.message(Command("log_workout"))
async def set_log_water(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, укажите время вашей тренировки")
    await message.answer("Введите время в мин:")
    await state.set_state(WorkoutState.log_workout)


@router.message(WorkoutState.log_workout)
async def process_workout(message: Message, state: FSMContext):
    try:
        workout_time = int(message.text)
    except ValueError:
        await message.answer("Ошибка. Введите пожалуйста целое число:")
        return

    user_data = await state.get_data()

    await state.update_data(
        workout_today=user_data["workout_today"] + workout_time / 30 * 200
    )

    user_data = await state.get_data()

    await message.answer(
        f"Отлично! Сегодня вы сожгли уже {user_data["workout_today"]} ккал из {user_data["calories_norm"]} ккал"
    )
