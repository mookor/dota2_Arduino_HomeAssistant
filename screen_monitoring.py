from easy_udp import UDPSender
from config import APPS_USB_PORT
import pyautogui
import time


class ScreenMonitoring:
    sender = UDPSender(host="localhost", port=APPS_USB_PORT)
    rosh_killed = False
    rosh_time = 7*60
    rosh_killed_time = 0
        

    @classmethod
    def check_rosh_killed(cls):
        while True:
            if not cls.rosh_killed:
                try:
                    rosh_on_screen = pyautogui.locateOnScreen("data/roshan.png", confidence=0.7)
                    if rosh_on_screen:
                        cls.sender.send('r\n')
                        cls.rosh_killed = True
                        cls.rosh_killed_time = time.time()
                except KeyboardInterrupt:
                    break
                except:
                    pass
            else:
                if time.time() - cls.rosh_killed_time > cls.rosh_time:
                    cls.rosh_killed = False
                    
            time.sleep(0.01)    
