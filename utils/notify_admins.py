import logging

from aiogram import Dispatcher

from settings.config import settings


async def on_startup_notify(dp: Dispatcher):
    for admin in settings.admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)
