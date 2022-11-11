#include <Arduino.h>

#include "util.hpp"
#include "video1.hpp"

#define FRAME_Z 8
#define CHUNK_Z 8

uint8_t _chars[FRAME_Z + 1][CHUNK_Z];
uint8_t *chars = (uint8_t *) _chars;

void frame(ConvenientLCD &lcd, uint_farptr_t data, uint32_t frame) {
  memcpy_PF(chars, data + (frame * FRAME_Z * CHUNK_Z), FRAME_Z * CHUNK_Z);

  for (uint8_t i = 0; i < CHUNK_Z; ++i) {
    lcd.createChar(i, _chars[i]);
  }

  lcd.print_(12, 0, (char) 0);
  lcd.print_(13, 0, (char) 1);
  lcd.print_(14, 0, (char) 2);
  lcd.print_(15, 0, (char) 3);
  lcd.print_(12, 1, (char) 4);
  lcd.print_(13, 1, (char) 5);
  lcd.print_(14, 1, (char) 6);
  lcd.print_(15, 1, (char) 7);
}

void play(ConvenientLCD &lcd, uint_farptr_t data, uint32_t frames) {
  for (uint32_t i = 0; i < frames; ++i) {
    frame(lcd, data, i);
    delay(125);
  }
}

ConvenientLCD lcd(22, 24, 26, 28, 30, 32, 34);

void setup() {
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print_(0, 0, "BAD        \xFF");
  lcd.print_(0, 1, "APPLE!     \xFF");
}

void loop() {
  play(lcd, pgm_get_far_address(video1a), 128);
  play(lcd, pgm_get_far_address(video1b), 128);
  play(lcd, pgm_get_far_address(video1c), 128);
  play(lcd, pgm_get_far_address(video1d), 128);
  play(lcd, pgm_get_far_address(video1e), 128);
  play(lcd, pgm_get_far_address(video1f), 128);
  play(lcd, pgm_get_far_address(video1g), 128);
  play(lcd, pgm_get_far_address(video1h), 128);
  play(lcd, pgm_get_far_address(video1i), 128);
  play(lcd, pgm_get_far_address(video1j), 128);
  play(lcd, pgm_get_far_address(video1k), 128);
  play(lcd, pgm_get_far_address(video1l), 128);
  play(lcd, pgm_get_far_address(video1m), 128);
  play(lcd, pgm_get_far_address(video1n),  89);
  delay(5000);
}
