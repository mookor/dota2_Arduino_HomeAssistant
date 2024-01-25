from bot.loader import bot
from bot.keyboards.keyboards import main_keyboard, additional_keyboard
from bot.utils.get_data import get_data, get_last_stats
from bot.utils.graph import draw_graph
from bot.config import plot_path
from logger import Logger

user_content = {}

@bot.message_handler(commands=["start"])
def start(message):
    user_content[message.chat.id] = {}
    bot.send_message(message.chat.id, "Hello, " + message.from_user.first_name, reply_markup=main_keyboard())
    Logger.info("User " + str(message.chat.id) + " started bot")

def first_step(message):
    
    
    if message.text == "💦 Влажность":
        user_content[message.chat.id]["type"] = "humidity"
    elif message.text == "🌡️ Температура":
        user_content[message.chat.id]["type"] = "temperature"

    bot.send_message(message.chat.id, "За какое время", reply_markup=additional_keyboard())
    Logger.info("User " + str(message.chat.id) + " chose first step")

def fill_time(message):
    time_dict = {"Час" : "hour", 
                 "12 часов" : "half_day", 
                 "Сутки" : "day", 
                 "Неделя" : "week", 
                 "30 дней" : "month"}
    user_content[message.chat.id]["time"] = time_dict[message.text]

def print_stat(chat_id):
    temperature, humidity = get_last_stats()
    bot.send_message(chat_id, f"🔥Температура: {temperature}°C\n💧Влажность: {humidity}%")
    Logger.info("User " + str(chat_id) + " printed stats")

@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "📊 Текущие показатели":
        print_stat(message.chat.id)

    elif message.text == "↩️ Назад":
        bot.send_message(message.chat.id, "Выберите тип", reply_markup=main_keyboard())

    elif message.chat.id not in user_content:
        bot.send_message(message.chat.id, "Нажми /start")
    else:
        if message.text in ["💦 Влажность", "🌡️ Температура"]:
            first_step(message)

        elif message.text in ["Час", "12 часов", "Сутки", "Неделя", "30 дней"]:
            
            fill_time(message)
            time_interval = user_content[message.chat.id]["time"]
            meassure_type = user_content[message.chat.id]["type"]
            
            flatten_data, dates = get_data(time_interval, meassure_type)
            if draw_graph(flatten_data, dates, meassure_type):
                maximum = max(flatten_data)
                minimum = min(flatten_data)
                try:
                    with open(plot_path, "rb") as photo:

                        Logger.info("Sending photo")
                        if meassure_type == "temperature":
                            bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f'🔥 Max 🔥 : *{maximum}*\n❄️ Min ❄️ : *{minimum}*\n❗️ Now ❗️ : *{flatten_data[-1]}*', parse_mode='Markdown', timeout=100)
                        else:
                            bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f'🌧️ Max 🌧️ : *{maximum}*\n💧 Min 💧 : *{minimum}*\n❗️ Now ❗️ : *{flatten_data[-1]}*', parse_mode='Markdown', timeout=100)
                except Exception as e:
                    Logger.info("Can't send photo: " + str(e))
                    bot.send_message(message.chat.id, "Не могу отправить график")
                    bot.send_message(message.chat.id, f'Max : *{maximum}*\nMin : *{minimum}*\n Now  : *{flatten_data[-1]}*', parse_mode='Markdown')
            else:
                bot.send_message(message.chat.id, "Данные не были получены")  
    

    # 
