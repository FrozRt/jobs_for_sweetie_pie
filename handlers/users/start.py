from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, text

from core.loader import dp
from handlers.channels.hh_vacancies_parser import parser
from handlers.channels.message import message_maker


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    msg = text(bold("Я могу ответить на следующие команды:"), "/help", "/start", sep="\n")
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text == "test")
async def test_action(message: types.Message):
    await parser.get_channels()


@dp.message_handler(lambda message: message.text == "mess")
async def test_action(message: types.Message):
    await message_maker.send_message()


@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        "Действие отменено. Введите /start, чтобы начать заново.",
        reply_markup=remove_keyboard,
    )
