#include <Arduino.h>
#include <LiquidCrystal.h>

class ConvenientLCD : public LiquidCrystal {
public:
  using LiquidCrystal::LiquidCrystal;

  void print_(uint8_t x, uint8_t y, char c) {
    setCursor(x, y);
    print(c);
  }

  void print_(uint8_t x, uint8_t y, const char *s) {
    setCursor(x, y);
    print(s);
  }
};
