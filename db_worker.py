from database import WeatherDatabase
from datetime import datetime
from easy_udp import UDPReceiver, UDPSender
import numpy as np
import time
from config import USB_DBWORKER_PORT, BOT_DBWORKER_PORT, DBWORKER_BOT_PORT

class DatabaseWorker:
    def __init__(self):
        self.db = WeatherDatabase()
        self.USB_receiver = UDPReceiver(host="localhost", port=USB_DBWORKER_PORT)
        self.BOT_receiver = UDPReceiver(host="localhost", port=BOT_DBWORKER_PORT)
        self.BOT_sender = UDPSender(host="localhost", port=DBWORKER_BOT_PORT)

    def __process_usb_data(self):
        received_data = self.USB_receiver.receive()
        if received_data is not None:
            humidity, temperature = received_data
            self.db.add_row(datetime.now(), humidity, temperature)

    def __process_bot_data(self):
        received_data = self.BOT_receiver.receive()
        
        if received_data is not None:
            if isinstance(received_data, str):
                if received_data == 'current':
                    msg = np.array((self.db.get_last_row()))
                    self.BOT_sender.send(msg)
            else:
                start_date, end_date = received_data
                msg = np.array((self.db.get_data_in_range(start_date, end_date)))
                msg = msg.flatten()
                msg = "_".join(msg)
                if len(msg) > 0:
                    self.BOT_sender.send(msg)

    def run(self):
        while True:
            self.__process_usb_data()
            self.__process_bot_data()
            time.sleep(0.01)

if __name__ == '__main__':
    db_worker = DatabaseWorker()
    db_worker.run()