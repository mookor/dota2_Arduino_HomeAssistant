#include <iarduino_AM2320.h> 

struct wether_sensor_data
{
    float temperature;
    float humidity;
};

void init_sensor();
wether_sensor_data get_wether();
