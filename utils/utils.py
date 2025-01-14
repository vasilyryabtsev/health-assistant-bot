import sys
import os
import asyncio
import aiohttp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import OPENWEATHER_API_KEY, OPENWEATHER_API_URL

def get_lat_lon(city):
    """
    Получить широту и долготу города.
    """
    pass

async def get_weather(latitude, longitude):
    """
    Получить температуру по широте и долготе.
    """
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(OPENWEATHER_API_URL, params=params, timeout=10) as response:
                if response.status != 200:
                    return {}
                data = await response.json()
                main = data.get('main', {})
                return main.get('temp')
        except aiohttp.ClientError as e:
            print(f"Ошибка клиента OpenWeatherAPI: {e}")
            return {}
        except asyncio.TimeoutError:
            print("Ошибка: Таймаут при запросе к OpenWeatherAPI")
            return {}
