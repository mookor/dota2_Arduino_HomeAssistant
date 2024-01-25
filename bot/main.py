import bot.messages
from bot.loader import bot
from logger import Logger
import time

def start_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            Logger.error('Error while polling - BOT DIED')
            time.sleep(1)
            
if __name__ == '__main__':
    Logger.info('Starting bot...')
    bot.infinity_polling()