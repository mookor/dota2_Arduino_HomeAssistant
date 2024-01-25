#include "wether.h"
iarduino_AM2320 sensor; 

void init_sensor()
{
    sensor.begin();
}



wether_sensor_data get_wether()
{
    
    float temperature = 0;
    float humidity =0;
    if (sensor.read() == AM2320_OK)
    {
        temperature = sensor.tem;
        humidity = sensor.hum;
        Serial.println((String) "t:" + temperature + " h:" + humidity);
    }
    wether_sensor_data data;
    data.temperature = temperature;
    data.humidity = humidity;
    return data;
    
}