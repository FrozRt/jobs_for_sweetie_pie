import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils.exceptions import RetryAfter
from aiogram.utils.markdown import bold, italic, text

from core.loader import dp
from handlers.channels.hh_vacancies_parser import parser


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    msg = text(bold("Я могу ответить на следующие команды:"), "/help", "/start", sep="\n")
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        "Действие отменено. Введите /start, чтобы начать заново.",
        reply_markup=remove_keyboard,
    )


@dp.message_handler(lambda message: message.text == "Parse")
async def whatsup_message(message: types.Message):
    await message.answer("Секунду")
    data = await parser.get_data()
    for vacancy in data:
        try:
            await message.answer(
                f"{vacancy['link_title']}\n"
                f"<b>{vacancy['salary']}</b>\r\n"
                f"\r\n"
                f"Организация: {vacancy['company_link_title']}\n"
                f"{vacancy['company_location']}\r\n"
                f"\r\n"
                f"{vacancy['work_responsibilities']}\n"
                f"\r\n"
                f"{vacancy['work_requirements']}",
                parse_mode="HTML",
            )
            await asyncio.sleep(0.1)
        except RetryAfter as e:
            await asyncio.sleep(e.timeout + 0.1)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(
        italic("Я не знаю, что с этим делать \nЯ просто напомню, что есть"),
        bold("команда:"),
        "/help",
    )
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)
