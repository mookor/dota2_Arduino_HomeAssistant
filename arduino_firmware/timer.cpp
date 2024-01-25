#include <stdint.h>
#include "timer.h"
MicroDS3231 rtc;

void rtc_set_time()
{
    rtc.setTime(BUILD_SEC, BUILD_MIN, BUILD_HOUR, BUILD_DAY, BUILD_MONTH, BUILD_YEAR);
}

uint32_t get_unix()
{ 
  return rtc.getUnix(7);
}

uint8_t get_month()
{
  return rtc.getMonth();
}

uint8_t get_date()
{
  return rtc.getDate();
}

String get_time_string()
{
  return rtc.getTimeString();
}
time get_seconds_to_moment(uint32_t start_time, int duration)
{
  uint32_t now = get_unix();
  uint32_t elapsed_time = duration - (now - start_time) % duration;
  uint32_t seconds = elapsed_time % 60;
  uint32_t minutes = elapsed_time / 60;
 
  time return_time;
  return_time.seconds = seconds;
  return_time.minutes = minutes;

  return return_time;
}