from pystray import MenuItem as item
import keyboard
from threading import Thread
from pc_controller.arduino import Arduino_controller
from pc_controller.screen_monitoring import Screen
import time
from bot.main import start_bot

class App:
    START_GAME_HOTKEY = 'F6'
    ROSH_KILLED_HOTKEY = 'F7'
    SOUND_HOTKEY = 'F2'

    def __init__(self):
        self.start_by_button = False

        self.arduino_controller = Arduino_controller()
        self.arduino_controller.start_temp_humidity_monitoring()
        self.screen = Screen(self.arduino_controller)
        self.screen.start_threads()

        self.hotkey_handler(self.START_GAME_HOTKEY, self.press_start_button)
        self.hotkey_handler(self.ROSH_KILLED_HOTKEY, self.press_rosh_button)
        self.hotkey_handler(self.SOUND_HOTKEY, self.sound)
        self.bot_thread = Thread(target=start_bot).start()
   
    
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

a = App()
