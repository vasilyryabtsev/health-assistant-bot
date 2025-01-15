from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Обработчик команды /start
@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply('''Welcome! I am your personal assistant for a healthy lifestyle!
Enter /help to find out my capabilities.''')
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply('''I can help you with the following commands:
/start - start the bot
/help - get help''')
    
# Функция для подключения обработчиков
def setup_handlers(dp):
    dp.include_router(router)