from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Dict
from utils.weather import get_lat_lon
    
class IsNumericFilter(BaseFilter):
    async def __call__(self, message: Message) -> Dict[str, int] | bool:
        try:
            return {'number': int(message.text)}
        except ValueError:
            await message.reply("Please enter a number")
            return False
        
class InListFilter(BaseFilter):
    def __init__(self, list: list):
        self.list = list
        
    async def __call__(self, message: Message) -> bool:
        if message.text in self.list:
            return True
        else:
            await message.reply(f"Please enter one of the following values: {', '.join(self.list)}")
            return False
        
class CityNameFilter(BaseFilter):
    async def __call__(self, message: Message) -> Dict[str, str] | bool:
        city = message.text.capitalize()
        lat, _ = await get_lat_lon(city)
        if lat is not None:
            return {'city': city}
        else:
            await message.reply("City not found")
            return False