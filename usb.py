import re
import serial
import serial.tools.list_ports
from easy_udp import UDPSender, UDPReceiver
import numpy as np
import time
from config import USB_DBWORKER_PORT, APPS_USB_PORT
from datetime import datetime, timedelta
import threading 

class USB:
    def __init__(self) -> None:
        self.comport = self.__init_comport()
        self.sender = UDPSender(host="localhost", port=USB_DBWORKER_PORT)
        self.receiver = UDPReceiver(host="localhost", port=APPS_USB_PORT)
        self.time_uptime = 0  # in days
        self.last_uptime = datetime.now() - timedelta(days=1)


        if self.comport:
            self.ser = serial.Serial(self.comport, 9600)
        else:
            raise Exception("No Arduino connected")


    def __init_comport(self):
        arduino_ports = [
            p.name 
            for p in serial.tools.list_ports.comports()
            if "CH340" in p.description
        ]
        return arduino_ports[0] if arduino_ports else None
    


    def __reciever_cycle(self):
        while True:
            try:
                app_data = self.receiver.receive()
                if app_data is not None:
                    app_data = app_data.encode('utf-8')
                    self.ser.write(app_data)

            except KeyboardInterrupt:
                break
            time.sleep(0.01)

    def __usb_cycle(self):
        while True:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                self.ser.flush()
                
                if len(line) and 'y' not in line:
                    str_values = re.findall(r'\d+\.\d+|\d+', line)
                    values = np.array([float(x) for x in str_values])
                    if len(values):
                        self.sender.send(values)

                uptime_delta = datetime.now() - self.last_uptime

                if  uptime_delta.days > self.time_uptime:
                    self.__update_time()
                    self.last_uptime = datetime.now()

            except KeyboardInterrupt:
                break
            time.sleep(0.01)

    def __update_time(self):
        current_datetime = datetime.now().strftime('s:%S m:%M h:%H d:%d min:%m y:%Y')
        current_datetime += '\n'
        self.ser.write(current_datetime.encode())

    def run(self):
        t1 = threading.Thread(target=self.__reciever_cycle)
        t2 = threading.Thread(target=self.__usb_cycle)
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__ == "__main__":
    obj = USB()
    obj.run()