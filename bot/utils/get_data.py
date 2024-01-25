from datetime import datetime, timedelta
from database.database import WeatherDatabase
from logger import Logger

def get_time_delta(time_interval):
    hours_dict = {
                    "hour" : 1, 
                    "half_day" : 12, 
                    "day" : 24, 
                    "week" : 168, 
                    "month" : 720
                 }
    delta = datetime.now() - timedelta(hours=hours_dict[time_interval])
    return delta

def correct_output(data, time_interval):
    if time_interval in ["hour", "half_day", "day"]:
        data = [i[0][-8:-3] for i in data]
    elif time_interval == "week": 
        data = [i[0][5:13] for i in data]
    elif time_interval == "month": 
        data = [i[0][5:10] for i in data]
    return data

def get_data(time_interval, meassure_type):
    delta = get_time_delta(time_interval)

    Logger.info("Getting data in range: " + delta.strftime('%Y-%m-%d %H:%M:%S') + " - " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    weather_db = WeatherDatabase()
    data_in_range = weather_db.get_data_in_range(delta.strftime('%Y-%m-%d %H:%M:%S'), 
                                                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    if len(data_in_range) == 0:
        Logger.info("Empty data in range")
        return [], []
    
    if meassure_type == "humidity":
        flatten_data = [i[1] for i in data_in_range]
    elif meassure_type == "temperature":
        flatten_data = [i[2] for i in data_in_range]

    dates = correct_output(data_in_range, time_interval)
    
    Logger.info("Got data in range")

    return flatten_data, dates

def get_last_stats():
    weather_db = WeatherDatabase()
    last_data = weather_db.get_last_row()
    temperature = last_data[2]
    humidity = last_data[1]
    return temperature, humidity