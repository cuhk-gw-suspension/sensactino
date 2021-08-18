#include "AD5662.h"
#include "DirectAccess.h"

// ad5662 write sequence's bit length 
const uint8_t LEN = 24;

/* template <typename T> */
void actuate(uint16_t val, uint8_t din, uint8_t sclk, uint8_t sync){
  setOutputPin(sync, LOW);
  _writeByte(din, sclk, 0x00);
  _writeByte(din, sclk, (val >> 8) & 0xFF);
  _writeByte(din, sclk, val & 0xFF);
  setOutputPin(sync, HIGH);
}

void _writeByte(uint8_t din, uint8_t sclk, uint8_t thebyte) {
  for (uint8_t j = 0; j < 8; j++) {
      setOutputPin(sclk, HIGH);
      delayMicroseconds(1);
      setOutputPin(din, (thebyte >> (7 - j)) & 0x01);
      delayMicroseconds(1);
      setOutputPin(sclk, LOW);
  }
}
