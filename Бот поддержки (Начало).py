from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *


api = '7908984850:AAFibL_LWxJdzWXwTP-xKbWlFPPXsiIRTv0'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Регистрация')
kb.add(button)
kb.add(button2)


initiate_db()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Добро пожаловать! Нажмите "Регистрация" для создания аккаунта', reply_markup=kb)


@dp.message_handler(text=['Регистрация'])
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    username = message.text
    if is_included(username):
        await message.answer('Пользователь существует, введите другое имя')
        return

    await state.update_data(username=username)
    await message.answer('Введите свой email:')
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    email = message.text
    await state.update_data(email=email)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    age = message.text
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    add_user(username, email,age)

    await message.answer('Вы успешно зарегистрированы!')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)