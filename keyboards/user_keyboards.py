from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def simple_kb():
    kb_list = [[KeyboardButton(text="Yes"), KeyboardButton(text="No")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Choose one of the options:"
    )
    
def gender_kb():
    kb_list = [[KeyboardButton(text='Male'), KeyboardButton(text='Female')]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Choose your gender:"
    )