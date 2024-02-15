from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from conder import getTemperature, getRotation, getCondition, getAlarams


token = '5884178179:AAH3vk1wVcTd7abUtrNdcglDl_1_0q70N4w'

bot = Bot(token=token)
dp = Dispatcher(bot)


# START_MENU
@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ['Кондиціонер', 'ІБП', 'Датчик температури', 'Додати/Видалити девайс']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Девайси", reply_markup=keyboard)


# CONDER_MENU
@dp.message_handler(Text(equals='Кондиціонер'))
async def conder(message: types.Message):
    conder_buttons = ['Температура', 'Стан', 'Обертання', 'Попереднє меню']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*conder_buttons)
    await message.answer("Кондеціонер", reply_markup=keyboard)


@dp.message_handler(Text(equals='Температура'))
async def temperature_conder(message: types.Message):
    await message.answer(getTemperature())


@dp.message_handler(Text(equals='Стан'))
async def condition_conder(message: types.Message):
    await message.answer(getCondition())


@dp.message_handler(Text(equals='Обертання'))
async def rotation_conder(message: types.Message):
    await message.answer(getRotation())


@dp.message_handler(Text(equals='Попереднє меню'))
async def back_device_conder(message: types.Message):
    await start(message)


@dp.message_handler(Text(equals='ІБП'))
async def ups(message: types.Message):
    ups_buttons = ['172.18.97.21', '172.18.97.22', '172.18.97.23', 'Попереднє меню']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*ups_buttons)
    await message.answer("ІБП", reply_markup=keyboard)

#_key_ip-UPS
@dp.message_handler(Text(equals='172.18.97.21'))
async def ups(message: types.Message):
    ups_buttons = ['функція1', 'функція2', 'функція3', 'Попереднє меню']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*ups_buttons)
    await message.answer("172.18.97.21", reply_markup=keyboard)

@dp.message_handler(Text(equals='172.18.97.22'))
async def ups(message: types.Message):
    ups_buttons = ['функція1', 'функція2', 'функція3', 'Попереднє меню']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*ups_buttons)
    await message.answer("172.18.97.22", reply_markup=keyboard)

@dp.message_handler(Text(equals='172.18.97.23'))
async def ups(message: types.Message):
    ups_buttons = ['функція1', 'функція2', 'функція3', 'Попереднє меню']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*ups_buttons)
    await message.answer("172.18.97.23", reply_markup=keyboard)

@dp.message_handler(Text(equals='Попереднє меню'))
async def back_device_conder(message: types.Message):
    await start(message)


# TEMP_SENSOR_MENU
@dp.message_handler(Text(equals='Датчик температури'))
async def sensor(message: types.Message):
    sensor_buttons = ['шото', 'шото', 'шото', 'шото', 'Back Device']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*sensor_buttons)
    await message.answer("Датчик температури", reply_markup=keyboard)


# ADD_REMOVE_MENU
@dp.message_handler(Text(equals='Додати/Видалити девайс'))
async def add_remove(message: types.Message):
    add_remove_buttons = ['Додати пристрій', 'Видалити пристрій', 'Back Device']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*add_remove_buttons)
    await message.answer("Додати/Видалити девайс", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
