from aiogram import Dispatcher
from loguru import logger

from .chat_filters import IsGroup
from .chat_filters import IsPrivate


def setup(dp: Dispatcher):
    logger.info("Подключение filters...")
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)