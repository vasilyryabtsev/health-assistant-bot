import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.new_user import router as new_user_router
from handlers.user import router as user_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(new_user_router)
dp.include_router(user_router)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())