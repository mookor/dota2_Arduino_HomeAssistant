from threading import Thread
import pyautogui
import time
from logger import Logger
pyautogui.useImageNotFoundException(0)
class Screen:
    def __init__(self, controller):
        self.arduino_controller = controller
        self.game_started = False
        self.rosh_killed = False
        self.start_thread = Thread(target=self.check_started)
        self.rosh_thread = Thread(target=self.check_rosh_killed)
    def check_started(self):
        while True:
            if not self.game_started:
                print("try to start game")
                start_on_screen = pyautogui.locateOnScreen("pc_controller/dota_start_time.png", confidence=0.9,) #  region=(1250, 25, 100, 400)
                if start_on_screen is not None:
                    self.game_started = True
                    Logger.info("Game started!")
                    self.arduino_controller.start_game()
            # else:
            #     Logger.info("break game_started")
            #     break
            time.sleep(0.01)
    
    def check_rosh_killed(self):
        while True:
            if self.game_started and not self.rosh_killed:
                print("try to roshan")
                rosh_on_screen = pyautogui.locateOnScreen("pc_controller/roshan.png", confidence=0.7, ) # region=(0, 750, 300, 400) 
                if rosh_on_screen is not None:
                    self.rosh_killed = True
                    Logger.info("Roshan killed!")
                    self.arduino_controller.rosh_killed()
            # else:
            #     Logger.info("break rosh_killed")
            #     break
            time.sleep(0.01)

    def start_threads(self):
        self.start_thread.start()
        self.rosh_thread.start()

    def stop_all_threads(self, game, rosh):
        self.game_started = True
        self.rosh_killed = True
        self.start_thread.join()
        self.rosh_thread.join()
        self.game_started = game
        self.rosh_killed = rosh
        time.sleep(0.01)
        Logger.info("All threads stopped")


