from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_ras = KeyboardButton(text="Рассчитать")
button_info = KeyboardButton(text="Информация")
kb.row(button_ras)
kb.row(button_info)


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)
    await message.answer('Введите "Рассчитать" что бы начать рассчет вашей нормы каллорий')

@dp.message_handler(text = 'Информация')
async def InFo(message):
    await message.answer("Тут скоро появится информация!")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()

@dp.message_handler(text= 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth= message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight= message.text)
    await message.answer('Введите пол "м" или "ж":')
    await UserState.sex.set()

@dp.message_handler(state= UserState.sex)
async def send_calories(message, state):
    await state.update_data(sex= message.text)
    data = await state.get_data()
    if data["sex"].lower() == "м":
        calories_men = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
        await message.answer(f'Ваша норма колорий: {calories_men}')
    if data["sex"].lower() == "ж":
        calories_women = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
        await message.answer(f'Ваша норма колорий: {calories_women}')
        await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)