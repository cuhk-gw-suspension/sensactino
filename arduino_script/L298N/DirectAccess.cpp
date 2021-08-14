#include "DirectAccess.h"


void initOutputPin(uint8_t pin) {
  if (pin < 8)
    DDRD |= (1 << pin);
  else if (pin < 14){
    pin -= 8;
    DDRB |= (1 << pin);
  }
  else if (pin >= 160 && pin < 168){
    pin -= 160;
    DDRC |= (1 << pin);
  }
}


// set outputPin as HIGH or LOW.
void setOutputPin(uint8_t pin, bool state){
  volatile uint8_t *addrToDataRegister;
  if (pin < 8)
    addrToDataRegister = &PORTD;
  else if (pin < 14){
    pin -= 8;
    addrToDataRegister = &PORTB;
  }
  else if (pin >= 160 && pin < 168){
    pin -= 160;
    addrToDataRegister = &PORTC;
  }

  if (state)
      *addrToDataRegister |= (1 << pin); // wrtie HIGH to the pin
  else
      *addrToDataRegister &= ~(1 << pin); // write LOW to the pin
}


bool readPin(uint8_t pin){
  if (pin < 8)
    return ((PIND & (1 << pin)) >> pin);
  else if (pin < 14){
    pin -= 8;
    return ((PINB & (1 << pin)) >> pin);
  }
  else if (pin >= 160 && pin < 168){
    pin -= 160;
    return ((PINC & (1 << pin)) >> pin);
  }
}

