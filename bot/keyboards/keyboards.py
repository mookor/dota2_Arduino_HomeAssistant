
from telebot import types

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💦 Влажность")
    btn2 = types.KeyboardButton("🌡️ Температура")
    btn3 = types.KeyboardButton("📊 Текущие показатели")
    
    markup.add(btn1, btn2, btn3)
    return markup

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