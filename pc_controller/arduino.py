import serial
import serial.tools.list_ports
from datetime import datetime
from database.database import WeatherDatabase
import time
from threading import Thread
from logger import Logger

class Arduino_controller:
    def __init__(self):
        self.com_port = self.get_arduino_comport()
        self.weather_db = WeatherDatabase()
        if self.com_port:
            self.ser = serial.Serial(self.com_port, 9600)
        else:
            raise Exception("No Arduino connected")
    
    def start_temp_humidity_monitoring(self):
        self.th_thread = Thread(target=self.read_temperature_and_humidity).start()

    def get_arduino_comport(self):
        arduino_ports = [
            p.name 
            for p in serial.tools.list_ports.comports()
            if "CH340" in p.description
        ]
        return arduino_ports[0] if arduino_ports else None
    
    def start_game(self):
        Logger.info("write 5(start) to arduino")
        self.ser.write(b'5')
    
    def rosh_killed(self):
        
        Logger.info("write 2(rosh) to arduino")
        self.ser.write(b'2')

    def sound(self):
        self.ser.write(b'4')
    
    def read_temperature_and_humidity(self):
        while True:
            try:
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

