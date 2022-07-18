from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, text

from core.loader import dp


class OrderVacancy(StatesGroup):
    profession = State()
    city = State()
    salary = State()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Какую работу вы ищите?")
    await OrderVacancy.profession.set()


@dp.message_handler(state=OrderVacancy.profession)
async def choose_job(message: types.Message, state: FSMContext):
    await state.update_data(chosen_job=message.text)
    await message.answer("В каком городе вы ищите работу?")
    await OrderVacancy.city.set()


@dp.message_handler(state=OrderVacancy.city)
async def choose_city(message: types.Message, state: FSMContext):
    await state.update_data(chosen_city=message.text)
    await message.answer("Укажите ваши зарплатные ожидания.\nПример: 20000 - 30000")
    await OrderVacancy.salary.set()


@dp.message_handler(state=OrderVacancy.salary)
async def choose_city(message: types.Message, state: FSMContext):
    await state.update_data(chosen_salary=message.text)
    vacansy_filter_data = await state.get_data()
    print(2)


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
