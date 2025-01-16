from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.registration import UserProfile
from keyboards.user_keyboards import simple_kb, gender_kb
from utils.nutrition import calculate_calories_norm

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
/help - get help
/set_profile - set your profile''')
    
# FSM
@router.message(Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext):
    await message.reply('Choose your gender', reply_markup=gender_kb())
    await state.set_state(UserProfile.gender)

@router.message(UserProfile.gender)
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.reply("What's your weight (kg)?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserProfile.weight)
    
@router.message(UserProfile.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.reply('What is your height (cm)?')
    await state.set_state(UserProfile.height)
    
@router.message(UserProfile.height)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.reply('Enter your age:')
    await state.set_state(UserProfile.age)
    
@router.message(UserProfile.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.reply('Enter the average activity time per day for the week (minutes):')
    await state.set_state(UserProfile.activety_time)
    
@router.message(UserProfile.activety_time)
async def process_activety_time(message: Message, state: FSMContext):
    await state.update_data(activety_time=message.text)
    await message.reply('Do you want to set your own calorie goal?', reply_markup=simple_kb())
    await state.set_state(UserProfile.calories_goal_ind)
    
@router.message(UserProfile.calories_goal_ind)
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
            activety_time=int(data['activety_time'])
        )
        await state.update_data(calories_goal=norm)
        await message.reply('Enter your city:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserProfile.city)

@router.message(UserProfile.calories_goal)
async def process_calories_goal(message: Message, state: FSMContext):
    await state.update_data(calories_goal=message.text)
    await message.reply('Enter your city:')
    await state.set_state(UserProfile.city)

@router.message(UserProfile.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.reply('Your profile is set!')
    await state.clear()    
    
# Функция для подключения обработчиков
def setup_handlers(dp):
    dp.include_router(router)