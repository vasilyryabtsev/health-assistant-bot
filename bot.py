import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.user_router import setup_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

setup_handlers(dp)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())