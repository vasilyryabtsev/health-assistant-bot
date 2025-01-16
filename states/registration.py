from aiogram.fsm.state import State, StatesGroup

class UserProfile(StatesGroup):
    gender = State()
    weight = State()
    height = State()
    age = State()
    activity_time = State()
    calories_goal_ind = State()
    calories_goal = State()
    city = State()