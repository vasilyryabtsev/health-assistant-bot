import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
if not OPENWEATHER_API_KEY:
    raise ValueError("Переменная окружения OPENWEATHER_API_KEY не установлена!")