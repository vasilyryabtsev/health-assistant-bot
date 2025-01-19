from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from filters.types import InUsersFilter, IsNumberArgFilter, ArgFilter
from typing import Dict
from datetime import datetime
from utils.nutrition import calculate_water_norm, get_calories
from utils.workouts import get_burned_calories
from utils.progress import calculate_water_data, calculate_calories_data, get_water_progress, get_calories_progress

router = Router()
router.message.filter(InUsersFilter())

@router.message(Command('my_profile'))
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

@router.message(Command('remove_profile'))
async def cmd_remove_profile(message: Message, users: Dict[str, Dict]):
    users.pop(message.from_user.id)
    await message.reply('''
Your profile has been removed. To create new profile, enter /set_profile.
''')
    
@router.message(Command('log_water'), IsNumberArgFilter())
async def cmd_log_water(message: Message, volume: float, users: Dict[str, Dict]):
    user = users[message.from_user.id]
    water_norm = (datetime.now(), await calculate_water_norm(user['weight'],
                                                                user['activity_time'],
                                                                user['city']))
    if 'water_norm' not in user or user['water_norm'][-1][0].date() < datetime.now().date():
        user['water_norm'] = [water_norm]
    else:
        user['water_norm'].append(water_norm)
    
    water_data = (datetime.now(), volume)
    if 'water_balance' not in user:
        user['water_balance'] = [water_data]
    else:
        user['water_balance'].append(water_data)
    
    water_goal_today, water_balance_today = calculate_water_data(user)
    left_to_goal = water_goal_today - water_balance_today
    await message.reply(f'''💧 You just had drunk {volume} ml. Today water goal is {water_goal_today} ml''')
    await message.answer(f'''{max(0, left_to_goal)} ml left to reach your goal''')

@router.message(Command('log_food'), ArgFilter())
async def cmd_log_food(message: Message, args: str, users: Dict[str, Dict]):
    user = users[message.from_user.id]
    calories = await get_calories(args)
    if calories > 0:
        res = (datetime.now(), args, calories)
        if 'calories_balance' not in user:
            user['calories_balance'] = [res]
        else:
            user['calories_balance'].append(res)
        await message.reply(f'{args}: {calories} kcal added.')
    else:
        await message.reply(f'{args} not found.')
        
@router.message(Command('log_workout'), ArgFilter())
async def cmd_log_workout(message: Message, args: str, users: Dict[str, Dict]):
    user = users[message.from_user.id]
    name, time, calories = await get_burned_calories(args,
                                                     user['weight'],
                                                     user['height'],
                                                     user['age'])
    if calories > 0:
        res = (datetime.now(), name, time, calories)
        if 'burned' not in user:
            user['burned'] = [res]
        else:
            user['burned'].append(res)
        await message.reply(f'''{name} {time} min: {calories} kcal burned.''')
        if time > 0:
            volume = 200 * (time // 30)
            await message.answer(f'''💧 You need to drink {volume} ml of water after this.''')
    else:
        await message.reply('Try to enter the workout name again.')

@router.message(Command('check_progress'))
async def cmd_ckeck_progress(message: Message, users: Dict[str, Dict]):
    user = users[message.from_user.id]
    
    calories_goal = user['calories_goal']
    calories_current, burned_current = calculate_calories_data(user)
    
    water_goal_today, water_balance_today = calculate_water_data(user)
    
    print_data = get_water_progress(water_goal_today, water_balance_today)
    print_data += get_calories_progress(calories_goal, calories_current, burned_current)
    
    await message.reply(print_data)
