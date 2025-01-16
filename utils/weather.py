import sys
import os
import asyncio
import aiohttp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import OPENWEATHER_API_KEY, OPENWEATHER_API_URL, OPENWEATHER_GEO_API_URL

async def get_lat_lon(city):
    """
    Получить широту и долготу города.
    """
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(OPENWEATHER_GEO_API_URL, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if len(data) > 0:
                        return data[0]['lat'], data[0]['lon']
                    else:
                        return None, None
        except aiohttp.ClientError as e:
            print(f'Ошибка клиента OpenWeatherAPI: {e}')
        except asyncio.TimeoutError:
            print('Ошибка: Таймаут при запросе к OpenWeatherAPI')

async def get_weather(latitude, longitude):
    """
    Получить температуру в градусах цельсия по широте и долготе.
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
                if response.status == 200:
                    data = await response.json()
                    main = data.get('main', {})
                    return main.get('temp')
        except aiohttp.ClientError as e:
            print(f'Ошибка клиента OpenWeatherAPI: {e}')
        except asyncio.TimeoutError:
            print('Ошибка: Таймаут при запросе к OpenWeatherAPI')
        
async def get_weather_by_city(city):
    """
    Получить температуру по названию города.
    """
    lat, lon = await get_lat_lon(city)
    if not lat or not lon:
        return {}
    return await get_weather(lat, lon)
