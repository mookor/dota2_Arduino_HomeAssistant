import serial
import serial.tools.list_ports
from datetime import datetime
from datetime import timedelta
from database.database import WeatherDatabase
import time
from threading import Thread
from logger import Logger

class Arduino_controller:
    def __init__(self):
        self.com_port = self.get_arduino_comport()
        self.weather_db = WeatherDatabase()
        self.read_temperature_and_humidity_flag = True
        self.time_uptime = 0  # in days
        self.last_uptime = datetime.now() - timedelta(days=1)
        if self.com_port:
            self.ser = serial.Serial(self.com_port, 9600)
        else:
            raise Exception("No Arduino connected")
    
    def start_temp_humidity_monitoring(self):
        self.th_thread = Thread(target=self.read_temperature_and_humidity)
        self.th_thread.start()

    def stop_threads(self):
        Logger.info("Stop temperature and humidity monitoring...")
        self.read_temperature_and_humidity_flag = False
        self.th_thread.join()
        Logger.info("Temperature and humidity monitoring stopped")
        

    def get_arduino_comport(self):
        arduino_ports = [
            p.name 
            for p in serial.tools.list_ports.comports()
            if "CH340" in p.description
        ]
        return arduino_ports[0] if arduino_ports else None
    
    def start_game(self):
        Logger.info("write 5(start) to arduino")
        self.ser.write(b'g\n')
    
    def rosh_killed(self):
        
        Logger.info("write 2(rosh) to arduino")
        self.ser.write(b'r\n')

    def alarm(self):
        Logger.info("write a(alarm) to arduino")
        self.ser.write(b'a\n')
        
    def sound(self):
        self.ser.write(b'b\n')
    
    def send_datetime(self):
        current_datetime = datetime.now().strftime('s:%S m:%M h:%H d:%d min:%m y:%Y')
        current_datetime += '\n'
        print("current_datetime", current_datetime)
        self.ser.write(current_datetime.encode())

    def read_temperature_and_humidity(self):
        while self.read_temperature_and_humidity_flag:
            try:
                uptime_delta = datetime.now() - self.last_uptime
                if  uptime_delta.days > self.time_uptime:
                    self.send_datetime()
                    self.last_uptime = datetime.now()
                    print("send datetime")

                if self.ser:
                    data = self.ser.readline().decode('utf-8').strip()
                    self.ser.flush()

                    if data:
                        parts = data.split()
                        for part in parts:
                            key, value = part.split(':')
                            if key == 'h':
                                humidity = float(value)
                            elif key == 't':
                                temperature = float(value)
                        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        self.weather_db.add_row(current_datetime, humidity, temperature)
                        print(f"Humidity: {humidity}% | Temperature: {temperature}°C")
                    
                    
                        
            except Exception as e:
                print(e)
            time.sleep(1)

