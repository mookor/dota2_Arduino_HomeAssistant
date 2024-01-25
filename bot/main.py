import bot.messages
from bot.loader import bot
from logger import Logger
import time

class Bot:
    def __init__(self):
        pass
    def start_bot(self):
        Logger.info('Start polling...')
        bot.infinity_polling()

    def stop_bot(self):
        Logger.info('Stop polling...')
        bot.stop_polling()
        Logger.info('Bot stopped')
        

if __name__ == '__main__':
    Logger.info('Starting bot...')
    bot.infinity_polling()