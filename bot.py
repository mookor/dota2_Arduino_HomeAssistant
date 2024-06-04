from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import BotCommand
from aiogram.utils import executor
from dotenv import load_dotenv
from bot_states import States
import time
from easy_udp import UDPSender, UDPReceiver
from config import BOT_DBWORKER_PORT, DBWORKER_BOT_PORT
from datetime import datetime, timedelta
import os
import numpy as np

async def current_weather():
    sender.send("current")
    time.sleep(0.5)
    data = receiver.receive()
    temperature = data[1]
    humidity = data[2]
    return temperature, humidity

def get_time_delta(time_interval):
    time_dict = {"Час" : "hour", 
                 "12 часов" : "half_day", 
                 "Сутки" : "day", 
                 "Неделя" : "week", 
                 "30 дней" : "month"}
    
    hours_dict = {
                    "hour" : 1, 
                    "half_day" : 12, 
                    "day" : 24, 
                    "week" : 168, 
                    "month" : 720
                 }
    delta = datetime.now() - timedelta(hours=hours_dict[time_dict[time_interval]])
    return delta

async def setup_bot_commands(dp):
    bot_commands = [
        BotCommand(command="/start", description="Начать опрос"),
    ]
    await bot.set_my_commands(bot_commands)

def additional_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Час")
    btn2 = types.KeyboardButton("12 часов")
    btn3 = types.KeyboardButton("Сутки")
    btn4 = types.KeyboardButton("Неделя")
    btn5 = types.KeyboardButton("30 дней")
    btn6 = types.KeyboardButton("↩️ Назад")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💦 Влажность")
    btn2 = types.KeyboardButton("🌡️ Температура")
    btn3 = types.KeyboardButton("📊 Текущие показатели")
    
    markup.add(btn1, btn2, btn3)
    return markup

if load_dotenv():
    API_TOKEN = os.getenv("BOT_TOKEN")
else:
    os._exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
sender = UDPSender(host="localhost", port=BOT_DBWORKER_PORT)
receiver = UDPReceiver(host="localhost", port=DBWORKER_BOT_PORT)



@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    await message.answer("Choose what you want", reply_markup=main_keyboard())
    await States.choose.set()

@dp.message_handler(state=States.choose)
async def choose(message: types.Message, state: States.choose):
    if message.text == "💦 Влажность":
        await message.answer("Choose time interval:", reply_markup=additional_keyboard())
        await States.humidity.set()

    elif message.text == "🌡️ Температура":
        await message.answer("Choose time interval:", reply_markup=additional_keyboard())
        await States.temp.set()

    elif message.text == "📊 Текущие показатели":
        temperature, humidity = await current_weather()
        await message.answer(f"🔥 Температура: {temperature}°C\n💧Влажность: {humidity}%", reply_markup=main_keyboard())

@dp.message_handler(state=States.temp)
async def temperature(message: types.Message, state: States.temp):

    interval = get_time_delta(message.text)
    sender.send(np.array([str(interval), str(datetime.now())]))

    time.sleep(0.1)

    data = receiver.receive()
    
    if data is None:
        await message.answer("Нет данных")
    else:
        data = data.split('_')
        data = data[1::3]
        data = list(map(float, data))

        mean_data = sum(data) / len(data)

        await message.answer(f"🔥 Средняя температура за {message.text}: {mean_data:.2f}°C\n", reply_markup=main_keyboard())
    
    await States.choose.set()

@dp.message_handler(state=States.humidity)
async def humidity(message: types.Message, state: States.temp):

    interval = get_time_delta(message.text)
    sender.send(np.array([str(interval), str(datetime.now())]))

    time.sleep(0.1)

    data = receiver.receive()
    
    if data is None:
        await message.answer("Нет данных")
    else:
        data = data.split('_')
        data = data[2::3]
        data = list(map(float, data))

        mean_data = sum(data) / len(data)

        await message.answer(f"💧 Средняя влажность: за {message.text}: {mean_data:.2f}°C\n", reply_markup=main_keyboard())
    
    await States.choose.set()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)