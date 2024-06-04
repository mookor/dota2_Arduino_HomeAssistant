from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    choose = State()
    temp = State()
    humidity = State()