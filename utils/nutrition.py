import sys
import os
import asyncio
import aiohttp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import EDAMAM_APP_ID, EDAMAM_APP_KEY, EDAMAM_URL

async def get_calories(ingredient):
    """
    Получение информации о количестве калорий продукта или напитка.
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
                    return data.get('calories')
        except aiohttp.ClientError as e:
            print(f'Ошибка клиента EdamamAPI: {e}')
        except asyncio.TimeoutError:
            print('Ошибка: Таймаут при запросе к EdamamAPI')

def calculate_activity_coeff(activety_time):
    """
    Расчет коэффициента активности.
    """
    if activety_time > 12 * 60:
        return 1.9
    elif activety_time > 9 * 60:
        return 1.725
    elif activety_time > 6 * 60:
        return 1.55
    elif activety_time > 3 * 60:
        return 1.375
    else:
        return 1.2

def calculate_calories_norm(sex, weight, height, age, activety_time):
    """
    Расчет нормы калорий по формуле Харриса-Бенедикта.
    
    Параметры:
    weight - кг;
    height - см;
    age - полных лет;
    activity_time - время активности в неделю (минуты).
    """
    a = calculate_activity_coeff(activety_time)
    
    if sex == 'male':
        return a * (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age))
    else:
        return a * (447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age))
