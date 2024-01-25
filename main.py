from pystray import MenuItem as item
import keyboard
from threading import Thread
from pc_controller.arduino import Arduino_controller
from pc_controller.screen_monitoring import Screen
from bot.main import Bot

import signal
import sys
import os 
from logger import Logger

class App:
    START_GAME_HOTKEY = 'F6'
    ROSH_KILLED_HOTKEY = 'F7'
    SOUND_HOTKEY = 'F2'
    TERMINATE_HOTKEY = 'F10'

    def __init__(self):
        self.start_by_button = False

        self.arduino_controller = Arduino_controller()
        self.arduino_controller.start_temp_humidity_monitoring()
        self.screen = Screen(self.arduino_controller)
        self.screen.start_threads()
        self.bot = Bot()
        self.hotkey_handler(self.START_GAME_HOTKEY, self.press_start_button)
        self.hotkey_handler(self.ROSH_KILLED_HOTKEY, self.press_rosh_button)
        self.hotkey_handler(self.SOUND_HOTKEY, self.sound)
        self.hotkey_handler(self.TERMINATE_HOTKEY, self.terminate_program)

        self.bot_thread = Thread(target=self.bot.start_bot())
        self.bot_thread.start()
   
    
    def hotkey_handler(self, hotkey, func):
        keyboard.add_hotkey(hotkey, func)

    def press_start_button(self):
        self.arduino_controller.start_game()
        self.screen.game_started = not self.screen.game_started

    def press_rosh_button(self):
        self.arduino_controller.rosh_killed()
        self.screen.game_started = True
        self.screen.rosh_killed = True

    def sound(self):
        self.arduino_controller.sound()

    def terminate_program(self):
        Logger.info("Terminating program...")
        self.bot.stop_bot()

        self.screen.stop_all_threads()
        Logger.info("Screen thread joined")

        self.arduino_controller.stop_threads()
        Logger.info("Arduino thread joined")

        os.kill(os.getpid(), signal.SIGTERM)
        sys.exit(0)
        
a = App()
