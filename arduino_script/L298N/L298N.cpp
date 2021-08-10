#include "L298N.h"

void setPin(uint8_t pin, bool state){
    if (pin < 8){
      if (state)
          PORTD |= (1 << pin); // wrtie HIGH to the pin
      else
          PORTD &= ~(1 << pin); // write LOW to the pin
      }
    else if (pin < 14) {
      pin -= 8;
      if (state)
          PORTB |= (1 << pin); // wrtie HIGH to the pin
      else
          PORTB &= ~(1 << pin); // write LOW to the pin
      }
 } 

void actuate(long *val, uint8_t pins[2]){
  if (*val > 0){
    setPin(pins[0], HIGH);
    setPin(pins[1], LOW);
    OCR1A = (*val) & 0xFFFF;
  }
  else {
    setPin(pins[0], LOW);
    setPin(pins[1], HIGH);
    OCR1A = -(*val) & 0xFFFF;
  }
}
