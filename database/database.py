import sqlite3
from datetime import datetime

class WeatherDatabase:
    def __init__(self, db_name='weather_database.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                date DATETIME,
                weather REAL,
                humidity REAL
            )
        ''')
        self.conn.commit()

    def add_row(self, date, weather, humidity):
        self.cursor.execute('''
            INSERT INTO weather_data (date, weather, humidity)
            VALUES (?, ?, ?)
        ''', (date, weather, humidity))
        self.conn.commit()

    def get_data_in_range(self, start_date, end_date):
        print("start_date", start_date, "end_date", end_date)
        self.cursor.execute('''
            SELECT * FROM weather_data
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        print("Done getting data in range")
        return self.cursor.fetchall()

    def get_last_row(self):
        self.cursor.execute('''
            SELECT * FROM weather_data
            ORDER BY date DESC
            LIMIT 1
        ''')
        return self.cursor.fetchone()
    
    def close_connection(self):
        self.conn.close()