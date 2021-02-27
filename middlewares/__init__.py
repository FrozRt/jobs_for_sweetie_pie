from aiogram import Dispatcher
from loguru import logger

from settings.config import admins
from .middlewares import ThrottlingMiddleware, AccessMiddleware


def setup(dp: Dispatcher):
    logger.info("Подключение middlewares...")
    dp.middleware.setup(AccessMiddleware(admins))
    dp.middleware.setup(ThrottlingMiddleware())
