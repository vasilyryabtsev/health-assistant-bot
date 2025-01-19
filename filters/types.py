from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.filters.command import CommandObject
from typing import Dict
from utils.weather import get_lat_lon
    
class IsNumericFilter(BaseFilter):
    """
    Проверяет является ли сообщение числом.
    """
    async def __call__(self, message: Message) -> Dict[str, int] | bool:
        try:
            return {'number': int(message.text)}
        except ValueError:
            await message.reply("Please enter a number")
            return False
        
class InListFilter(BaseFilter):
    """
    Проверяет находится ли сообщение в списке.
    """
    def __init__(self, list: list):
        self.list = list
        
    async def __call__(self, message: Message) -> bool:
        if message.text in self.list:
            return True
        else:
            await message.reply(f"Please enter one of the following values: {', '.join(self.list)}")
            return False
        
class CityNameFilter(BaseFilter):
    """
    Фильтр для проверки существования города.
    """
    async def __call__(self, message: Message) -> Dict[str, str] | bool:
        city = message.text.capitalize()
        lat, _ = await get_lat_lon(city)
        if lat is not None:
            return {'city': city}
        else:
            await message.reply("City not found")
            return False
        
class InUsersFilter(BaseFilter):
    """
    Фильтр для проверки наличия пользователя в базе данных.
    """
    async def __call__(self, message: Message, users: Dict[int, Dict]) -> bool:
        user_id = message.from_user.id
        if user_id in users:
            return True
        else:
            await message.reply('You need to set yout profile first. Enter /set_profile')
            return False
        
class IsNotProfileFilter(BaseFilter):
    """
    Проверяет есть ли у пользователя профиль.
    """
    async def __call__(self, message: Message, users: Dict[int, Dict]) -> bool:
        user_id = message.from_user.id
        if user_id in users:
            await message.reply('You have already set your profile. To show it, enter /my_profile')
            return False
        else:
            return True

class IsNumberArgFilter(BaseFilter):
    """
    Проверяет является ли аргумент числом.
    """
    async def __call__(self, message: Message, command: CommandObject, users: Dict[int, Dict]) -> Dict[str, float] | bool:
        try:
            args = command.args.split()
            if len(args) > 1:
                await message.reply('Please enter only one number')
                return False
            volume = float(args[0])
            return {'volume': volume}
        except Exception:
            await message.reply('Please enter a number')
            return False
        
class ArgFilter(BaseFilter):
    """
    Проверяет наличие аргументов после команды.
    """
    async def __call__(self, message: Message, command: CommandObject) -> str | bool:
        if command.args is not None:
            return {'args': command.args}
        else:
            await message.reply('Please enter arguments after the command')
            return False