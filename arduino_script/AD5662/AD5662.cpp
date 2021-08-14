#include "AD5662.h"
#include "DirectAccess.h"

// ad5662 write sequence's bit length 
const uint8_t LEN = 24;

/* template <typename T> */
void actuate(uint16_t *val, uint8_t din, uint8_t sclk, uint8_t sync){
  setOutputPin(sync, LOW);
  _writeByte(din, sclk, 0x00);
  _writeByte(din, sclk, *val & 0xFF);
  _writeByte(din, sclk, (*val >> 8) & 0xFF);
  setOutputPin(sync, HIGH);
}

void _writeByte(uint8_t din, uint8_t sclk, uint8_t byte) {
  for (uint8_t j = 0; j < 8; i++) {
      setOutputPin(sclk, HIGH);
      setOutputPin(din, (byte >> j) & 0x01);
      setOutputPin(sclk, LOW);
  }
}

