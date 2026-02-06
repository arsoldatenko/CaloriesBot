from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.water import WaterState
from states.base import BaseState

router = Router()


@router.message(Command("log_water"))
async def set_log_water(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, укажите количество выпитой вами воды, оно будет суммировано с водой, которую вы сегодня выпили ранее"
    )
    await message.answer("Введите воду в мл:")
    await state.set_state(WaterState.log_water)


@router.message(WaterState.log_water)
async def process_water(message: Message, state: FSMContext):
    try:
        water_amount = float(message.text)
    except ValueError:
        await message.answer("Ошибка. Введите пожалуйста число:")
        return

    user_data = await state.get_data()

    await state.update_data(water_today=user_data["water_today"] + water_amount)

    user_data = await state.get_data()

    await message.answer(
        f"Отлично! Сегодня вы выпили уже {user_data["water_today"]} мл из {user_data["water_norm"]} мл"
    )
    await message.answer(
        f"Осталось выпить: {user_data["water_norm"] - user_data["water_today"]} мл"  # это бы вынести в отдельную функцию + добавить переполнение, но у меня нет времени :)
    )

    await state.set_state(BaseState.base)
