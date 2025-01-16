from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

router = Router()

@router.message(Command('my_profile'))
async def cmd_my_profile(message: Message):
    await message.reply('Your profile is empty. Enter /set_profile to set it up.')