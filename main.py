import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from routers import profile_router, water_router, workout_router
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(profile_router.router)
    dp.include_router(water_router.router)
    dp.include_router(workout_router.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
