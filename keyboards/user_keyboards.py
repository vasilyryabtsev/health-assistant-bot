from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def simple_kb():
    """
    Клавиатура для короткого ответа: Yes или No.
    """
    kb_list = [[KeyboardButton(text="Yes"), KeyboardButton(text="No")]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Choose one of the options:"
    )
    
def gender_kb():
    """
    Клавиатура для выбра пола: Male или Female.
    """
    kb_list = [[KeyboardButton(text='Male'), KeyboardButton(text='Female')]]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Choose your gender:"
    )