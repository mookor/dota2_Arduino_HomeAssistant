#include "WString.h"
#include "lcd.h"

LiquidCrystal_I2C lcd(0x27, 16, 2);

void init_lcd()
{
    lcd.init();
    lcd.backlight(); 
    lcd.setCursor(0, 0);
}

void clear_lcd()
{
    lcd.clear();
}

void print_lcd(String text, int x, int y)
{
    lcd.setCursor(x, y);
    lcd.print(text);
}
void print_lcd(int num, int x, int y)
{
    lcd.setCursor(x, y);
    lcd.print(num);
}