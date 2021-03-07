from aiogram import types
from aiogram.types import ParseMode
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic
from aiogram.dispatcher.filters.builtin import CommandStart

from core.loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/help', '/start', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)


# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(lambda message: message.text == "Отмена")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Действие отменено. Введите /start, чтобы начать заново.",
                         reply_markup=remove_keyboard)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(italic('Я не знаю, что с этим делать \nЯ просто напомню, что есть'),
                        bold('команда:'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

