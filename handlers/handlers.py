from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp

router = Router()

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Добро пожаловать! Я ваш бот.\nВведите /help для списка команд.")
    
# Функция для подключения обработчиков
def setup_handlers(dp):
    dp.include_router(router)