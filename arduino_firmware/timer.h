
#include <microDS3231.h>

struct time
{
    uint32_t seconds;
    uint32_t minutes;
};

void rtc_set_time(int8_t seconds, int8_t minutes, int8_t hours, int8_t date, int8_t month, int16_t year);
time get_seconds_to_moment(uint32_t start_time, int duration);
uint32_t get_unix();
uint8_t get_month();
uint8_t get_date();
String get_time_string();
