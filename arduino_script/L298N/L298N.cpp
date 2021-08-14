#include "L298N.h"
#include "DirectAccess.h"

void actuate(long *val, uint8_t pins[2]){
  if (*val > 0){
    setOutputPin(pins[0], HIGH);
    setOutputPin(pins[1], LOW);
    OCR1A = (*val) & 0xFFFF;
  }
  else {
    setOutputPin(pins[0], LOW);
    setOutputPin(pins[1], HIGH);
    OCR1A = -(*val) & 0xFFFF;
  }
}
