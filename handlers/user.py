from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from filters.types import InUsersFilter
from typing import Dict

router = Router()

@router.message(Command('my_profile'), InUsersFilter())
async def cmd_my_profile(message: Message, users: Dict[str, Dict]):
    user = users[message.from_user.id]
    await message.reply(f'''
📋 <b>Profile:</b>

🏙️ <b>City:</b> {user['city']}
🚻 <b>Gender:</b> {user['gender']}
🎂 <b>Age:</b> {user['age']} years
⚖️ <b>Weight:</b> {user['weight']} kg
📏 <b>Height:</b> {user['height']} cm
🏃 <b>Avg Activity Time:</b> {user['activity_time']} minutes per day
🍎 <b>Calories Norm:</b> {user['calories_goal']} kcal per day

🗑️ If you want to remove your profile, enter /remove_profile
''', parse_mode='HTML')
