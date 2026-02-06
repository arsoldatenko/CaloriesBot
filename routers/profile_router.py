from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.profile import ProfileState
from states.base import BaseState
from services.nsm_api import search_city
from services.calculations import calculated_calories_norm, calculated_water_norm
from keyboards.keyboards import gender_keyboard

router = Router()


@router.message(Command("set_profile"))
async def set_profile_start(message: Message, state: FSMContext):
    await message.answer("Обновим ваши параметры.")
    await message.answer("Введите ваш вес (кг):")
    await state.set_state(ProfileState.weight)


# Ввод веса
@router.message(ProfileState.weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
    except ValueError:
        await message.answer("Ошибка. Введите пожалуйста число:")
        return

    await state.update_data(weight=weight)
    await message.answer("Введите ваш рост (см):")
    await state.set_state(ProfileState.height)


# Ввод роста
@router.message(ProfileState.height)
async def process_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
    except ValueError:
        await message.answer("Ошибка. Введите пожалуйста число:")
        return

    await state.update_data(height=height)
    await message.answer("Введите ваш возраст:")
    await state.set_state(ProfileState.age)


# Ввод возраста
@router.message(ProfileState.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Ошибка. Введите пожалуйста целое число:")
        return

    await state.update_data(age=age)
    await message.answer("Введите вашу дневную активность в минутах:")
    await state.set_state(ProfileState.activity)


# Ввод активности
@router.message(ProfileState.activity)
async def process_activity(message: Message, state: FSMContext):
    try:
        activity = int(message.text)
    except ValueError:
        await message.answer("Ошибка. Введите пожалуйста целое число:")
        return

    await state.update_data(activity=activity)
    await message.answer("Выберите ваш пол:", reply_markup=gender_keyboard)
    await state.set_state(ProfileState.gender)


# Выбор пола
@router.callback_query(lambda c: c.data and c.data.startswith("gender_"))
async def process_gender(callback: types.CallbackQuery, state: FSMContext):
    gender = callback.data.split("_")[1]
    await state.update_data(gender=gender)
    await callback.message.delete()
    await callback.message.answer("Введите ваш город:")
    await state.set_state(ProfileState.city)


# Ввод города
@router.message(ProfileState.city)
async def process_city(message: Message, state: FSMContext):
    try:
        city = await search_city(str(message.text))
    except ValueError:
        await message.answer("Ошибка. Город не найден:")
        return

    await message.answer(f"Отлично, ваш город:")
    await message.answer(f"{city[0]["display_name"]}")
    await state.update_data(city=city[0]["display_name"])
    await state.set_state(BaseState.base)

    calories_norm = await calculated_calories_norm(await state.get_data())
    await message.answer(f"Ваша норма калорий: {calories_norm}")
    await state.update_data(calories_norm=calories_norm)
    await state.update_data(calories_today=0)  # пока так :)

    water_norm = await calculated_water_norm(await state.get_data())
    await state.update_data(water_norm=water_norm[0])
    await message.answer(
        f"Сегодня в вашем городе {water_norm[1]}, поэтому ваша норма воды: {water_norm[0]}"
    )
    await state.update_data(water_today=0)
    await message.answer("Отлично! Настройка профиля завершена.")

    await state.update_data(workout_today=0)
