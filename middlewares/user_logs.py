import logging
from aiogram import BaseMiddleware
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        logger.info(f"Получено сообщение от {event.from_user.id}: {event.text}")
        return await handler(event, data)