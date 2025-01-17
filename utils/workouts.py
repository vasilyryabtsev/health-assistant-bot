import os
import sys
import asyncio
import aiohttp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import NUTRITIONIX_URL, NUTRITIONIX_API_KEY, NUTRITIONIX_API_ID

def get_workout_data(text):
    """
    Возвращает данные о тренировке.
    """
    text_list = text.split(':')
    name = text_list[0]
    time = int(text_list[1])
    water = 200 * (time // 30) # 200 мл воды на каждые 30 минут тренировки
    return name, time, water

async def get_burned_calories(workout_info, weight, height, age):
    """
    Получить количество сожженных калорий.
    """
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': NUTRITIONIX_API_ID,
        'x-app-key': NUTRITIONIX_API_KEY
    }
    params = {
        'query': workout_info,
        'weight_kg': weight,
        'height_cm': height,
        'age': age
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(NUTRITIONIX_URL, json=params, headers=headers, timeout=10) as response:
            try:
                if response.status == 200:
                    data = await response.json()
                    exercises = data['exercises']
                    if len(exercises) > 0:
                        res = exercises[0]
                        return (res['name'], res['duration_min'], res['nf_calories'])
                    else:
                        return ('', 0, 0)
                else:
                    print(f'Ошибка: {response.status}')
            except aiohttp.ClientError as e:
                print(f'Ошибка клиента NutritionixAPI: {e}')
            except asyncio.TimeoutError:
                print('Ошибка: Таймаут при запросе к NutritionixAPI')
