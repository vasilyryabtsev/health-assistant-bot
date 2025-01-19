import sys
import os
import asyncio
import aiohttp
from utils.weather import get_weather_by_city

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import EDAMAM_APP_ID, EDAMAM_APP_KEY, EDAMAM_URL

async def get_calories(ingredient):
    """
    Получение информации о количестве калорий продукта или напитка (ккал).
    """
    params = {
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_APP_KEY,
        'nutrition-type': 'logging',
        'ingr': ingredient
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(EDAMAM_URL, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return round(data.get('calories'))
        except aiohttp.ClientError as e:
            print(f'Ошибка клиента EdamamAPI: {e}')
        except asyncio.TimeoutError:
            print('Ошибка: Таймаут при запросе к EdamamAPI')

def calculate_activity_coeff(activity_time):
    """
    Расчет коэффициента активности.
    
    Параметры:
    activity_time - время активности в неделю (часы).
    """
    if activity_time > 12:
        return 1.9
    elif activity_time > 9:
        return 1.725
    elif activity_time > 6:
        return 1.55
    elif activity_time > 3:
        return 1.375
    else:
        return 1.2

def calculate_calories_norm(gender, weight, height, age, activity_time):
    """
    Расчет нормы калорий в день по формуле Харриса-Бенедикта (ккал).
    
    Параметры:
    weight - кг;
    height - см;
    age - полных лет;
    activity_time - время активности в неделю (часы).
    """
    a = calculate_activity_coeff(activity_time)
    
    if gender == 'Male':
        return round(a * (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)))
    else:
        return round(a * (447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)))

async def calculate_water_norm(weight, activity_time, city):
    """
    Расчет нормы потребления воды в день (мл).
    
    Параметры:
    weight - кг.
    activity_time - время активности в день (минуты).
    city - город проживания.
    """
    temperature = await get_weather_by_city(city)
    
    temperature_coeff = 0
    if temperature >= 25:
        temperature_coeff = temperature / 25
    
    return round(weight * 30 + 500 * (activity_time / 30) + 500 * temperature_coeff)
