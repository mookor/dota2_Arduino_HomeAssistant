#include "lcd.h"
#include "timer.h"
#include "wether.h"
#include "GyverButton.h"

GButton butt1(4);
uint32_t start_game_unix = 0;
uint32_t kill_rosh_unix = 0;
uint32_t weather_millis;
uint32_t cycle_millis;

time to_rosh;
time to_exp;
time to_lotus;

float t = 0;
float h = 0;

bool rosh_died = false;
bool start = false;
bool songing = false;
bool led_up = true;
bool lotus = false;

const char* months[] =
 {"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};

void setup()
{
  Serial.begin(9600);

  butt1.setDebounce(40);        // настройка антидребезга (по умолчанию 80 мс)
  butt1.setTimeout(1000);        // настройка таймаута на удержание (по умолчанию 500 мс)
  butt1.setClickTimeout(600); 
  butt1.setType(HIGH_PULL);
  butt1.setDirection(NORM_OPEN);
  
  weather_millis = millis();
  cycle_millis = millis();
  init_sensor();
  init_lcd();
  
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  to_rosh.minutes = 1;
  to_rosh.seconds = 1;
}

void buttons(char signal)
{
    butt1.tick();  // обязательная функция отработки. Должна постоянно опрашиваться
    if (butt1.isDouble() || signal == '5')
    {
        start_game_unix = get_unix();
        start = !start;
        lotus = !lotus;
        clear_lcd();
    }
    if (butt1.isSingle() || signal == '2')
    {
        kill_rosh_unix = get_unix();
        start = true;
        rosh_died = true;
        clear_lcd();
    }
    if (butt1.isHolded() || signal == '4')
    {
        songing = !songing;
    }
}

void beep(time timing)
{
  if(songing)
    if (timing.minutes == 0 && 13 <= timing.seconds && timing.seconds <= 15)
      tone(11, 784, 1000);
  
}

void led_up_down()
{
  if(to_lotus.minutes == 0 && to_lotus.seconds <= 15 || to_exp.minutes == 0 && to_exp.seconds <= 15 || to_rosh.minutes == 0 && to_rosh.seconds <= 15)
  {
    digitalWrite(10, HIGH);
  }
  else
  {
    digitalWrite(10, LOW);
  }
}
void draw_lotus(time timing)
{
  print_lcd(" ", 5, 0);
  print_lcd((String) "l:" + timing.minutes + ":" + timing.seconds, 0, 0);
  beep(timing);
 
}

void draw_exp(time timing)
{
  print_lcd(" ", 5, 1);
  print_lcd((String) "e:" + timing.minutes + ":" + timing.seconds, 0, 1);
  beep(timing);
 
}

void draw_rosh(time timing_max)
{
  uint32_t min_rosh = 8 * 60;
  time timing_min = get_seconds_to_moment(kill_rosh_unix, min_rosh);
  String space = timing_max.minutes <= 9 ? ": " : ":";
  print_lcd(" ", 15, 0);
  print_lcd((String) "rmx" + space + timing_max.minutes + ":" + timing_max.seconds, 7, 0);
  if (timing_max.minutes > 3 && timing_max.seconds > 0)
  {
    print_lcd(" ", 15, 1);
    print_lcd((String) "rmn: " + timing_min.minutes + ":" + timing_min.seconds, 7, 1);
  }
  else
  {
    print_lcd("         ", 7, 1);
  }
  if (timing_max.minutes == 0 && timing_max.seconds <= 1)
  {
    rosh_died = false;
    print_lcd("         ", 7, 0);
  }
  beep(timing_max);
}

void loop()
{
  char signal = Serial.read();
  delay(20);
  buttons(signal);
  
  songing ? digitalWrite(9, HIGH): digitalWrite(9, 0);

  delay(20);
  if (millis() - weather_millis > 1000)
  {
    wether_sensor_data data = get_wether();
    t = data.temperature;
    h = data.humidity;
    weather_millis = millis();
  }
  if (millis() - cycle_millis > 1000)
  {
    delay(20);
    if (start)
    {

        if (lotus)
        { 
          to_lotus = get_seconds_to_moment(start_game_unix, 3 * 60);
          draw_lotus(to_lotus);
          to_exp = get_seconds_to_moment(start_game_unix, 7 * 60);
          draw_exp(to_exp);
        }
        if (rosh_died)
        {
          to_rosh = get_seconds_to_moment(kill_rosh_unix, 11 * 60);
          draw_rosh(to_rosh);
        }
        led_up_down();
    }
    else
    {
        if (rosh_died || lotus)
        {
          clear_lcd();
          rosh_died  = lotus = false;
        }
        print_lcd(get_date(), 0, 0);
        print_lcd(months[get_month()-1], 3, 0);
        print_lcd((String) " t:" + t, 8, 0);

        print_lcd(get_time_string(), 0, 1);
        print_lcd((String) "h:" + h, 9, 1);
        
    }
    cycle_millis = millis();
  }
}