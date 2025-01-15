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
