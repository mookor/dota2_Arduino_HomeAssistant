import keyboard
from config import APPS_USB_PORT
from easy_udp import UDPSender
from multiprocessing import Process
from screen_monitoring import ScreenMonitoring
import time

class KeyboardApp:
    START_STOP_GAME_HOTKEY = 'F6'
    ROSH_KILLED_HOTKEY = 'F7'
    SOUND_HOTKEY = 'F8'
    SCREEN_START_STOP_HOTKEY = 'F10'

    def __init__(self) -> None:
        self.sender = UDPSender(host="localhost", port=APPS_USB_PORT)
        self.screen_monitoring_status = True
        self.screen_monitoring_process = Process(target=ScreenMonitoring.check_rosh_killed, args=())

        self.__hotkey_handler(self.START_STOP_GAME_HOTKEY, self.__start_stop_game)
        self.__hotkey_handler(self.ROSH_KILLED_HOTKEY, self.__rosh_killed)
        self.__hotkey_handler(self.SOUND_HOTKEY, self.__sound)
        self.__hotkey_handler(self.SCREEN_START_STOP_HOTKEY, self.__screen_start_stop)

    def __hotkey_handler(self, hotkey, func):
        keyboard.add_hotkey(hotkey, func)

    def __start_stop_game(self):
        self.sender.send('g\n')
        time.sleep(0.1)

    def __rosh_killed(self):
        self.sender.send('r\n')
        time.sleep(0.1)

    def __sound(self):
        self.sender.send('b\n')
        time.sleep(0.1)
    
    def __screen_start_stop(self):
        if self.screen_monitoring_status:
            
            self.screen_monitoring_process.start()
            self.screen_monitoring_status = False
        else:
            self.screen_monitoring_process.terminate()
            self.screen_monitoring_process.join()
            self.screen_monitoring_process = Process(target=ScreenMonitoring.check_rosh_killed)
            self.screen_monitoring_status = True
        time.sleep(0.1)

    def run(self):
        while True:
            time.sleep(0.01)

if __name__ == '__main__':
    k = KeyboardApp()
    while True:
        time.sleep(0.01)