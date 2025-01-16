from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.registration import UserProfile
from keyboards.user_keyboards import simple_kb, gender_kb
from utils.nutrition import calculate_calories_norm
from filters.types import IsNumericFilter, InListFilter, CityNameFilter, IsNotProfileFilter
from typing import Dict

router = Router()

# Обработчик команды /start
@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply(f'''Welcome, {message.from_user.first_name}! 

I am your personal assistant for a healthy lifestyle!

Enter /help to find out my capabilities.''')
    
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply('''I can help you with the following commands:

/start - start the bot
/help - get help
/set_profile - set your profile
/my_profile - show my profile''')
    
# FSM
@router.message(Command('set_profile'), IsNotProfileFilter())
async def cmd_set_profile(message: Message, state: FSMContext):
    await message.reply('Choose your gender', reply_markup=gender_kb())
    await state.set_state(UserProfile.gender)

@router.message(UserProfile.gender, InListFilter(['Male', 'Female']))
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.reply("What's your weight (kg)?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserProfile.weight)
    
@router.message(UserProfile.weight, IsNumericFilter())
async def process_weight(message: Message, number: int, state: FSMContext):
    await state.update_data(weight=number)
    await message.reply('What is your height (cm)?')
    await state.set_state(UserProfile.height)
    
@router.message(UserProfile.height, IsNumericFilter())
async def process_height(message: Message, number: int, state: FSMContext):
    await state.update_data(height=number)
    await message.reply('Enter your age:')
    await state.set_state(UserProfile.age)
    
@router.message(UserProfile.age, IsNumericFilter())
async def process_age(message: Message, number: int, state: FSMContext):
    await state.update_data(age=number)
    await message.reply('Enter the average activity time per day for the week (minutes):')
    await state.set_state(UserProfile.activity_time)
    
@router.message(UserProfile.activity_time, IsNumericFilter())
async def process_activity_time(message: Message, number: int, state: FSMContext):
    await state.update_data(activity_time=number)
    await message.reply('Do you want to set your own calorie goal?', reply_markup=simple_kb())
    await state.set_state(UserProfile.calories_goal_ind)
    
@router.message(UserProfile.calories_goal_ind, InListFilter(['Yes', 'No']))
async def process_calories_goal_ind(message: Message, state: FSMContext):
    await state.update_data(calories_goal_ind=message.text)
    if message.text == 'Yes':
        await message.reply('Enter your calorie goal:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserProfile.calories_goal)
    else:
        data = await state.get_data()
        norm = calculate_calories_norm(
            gender=data['gender'],
            weight=int(data['weight']),
            height=int(data['height']),
            age=int(data['age']),
            activity_time=int(data['activity_time'])
        )
        await state.update_data(calories_goal=norm)
        await message.reply('Enter your city:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserProfile.city)

@router.message(UserProfile.calories_goal, IsNumericFilter())
async def process_calories_goal(message: Message, state: FSMContext):
    await state.update_data(calories_goal=message.text)
    await message.reply('Enter your city:')
    await state.set_state(UserProfile.city)

@router.message(UserProfile.city, CityNameFilter())
async def process_city(message: Message, city: str, users: Dict[int, Dict], state: FSMContext):
    await state.update_data(city=city)
    data = await state.get_data()
    data.pop('calories_goal_ind')
    users[message.from_user.id] = data
    await message.reply('Your profile is set! Enter /my_profile to view it.')
    await state.clear()