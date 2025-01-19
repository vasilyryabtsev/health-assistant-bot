import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
NUTRITIONIX_API_ID = os.getenv('NUTRITIONIX_API_ID')
NUTRITIONIX_API_KEY = os.getenv('NUTRITIONIX_API_KEY')

OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_GEO_API_URL = 'http://api.openweathermap.org/geo/1.0/direct'
EDAMAM_URL = 'https://api.edamam.com/api/nutrition-data'
NUTRITIONIX_URL = 'https://trackapi.nutritionix.com/v2/natural/exercise'

def validate_token(token):
    """
    Проверка наличия токена в переменной окружения.
    """
    if not token:
        raise ValueError(f'Переменная окружения {token} не установлена!')
    
validate_token('BOT_TOKEN')
validate_token('OPENWEATHER_API_KEY')
validate_token('EDAMAM_APP_ID')
validate_token('EDAMAM_APP_KEY')
validate_token('NUTRITIONIX_API_ID')
validate_token('NUTRITIONIX_API_KEY')
