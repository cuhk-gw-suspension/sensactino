#ifndef AD5662_h
    #define AD5662_h

#include <stdlib.h>
#if ARDUINO >= 100
    #include <Arduino.h>
#endif

// This defs cause troubles on some version of Arduino
#undef rounds

// copy from other, dont know why
#if (defined(ARDUINO) && ARDUINO >= 155) || defined(ESP8266)
    #define YIELD yield();
#else
    #define YIELD;
#endif

// select voltage based on the sign and magnitude of the passed value
void actuate(uint16_t val, uint8_t din, uint8_t sclk, uint8_t sync);

// write byte function for function actuate. byteorder: little
void _writeByte(uint8_t din, uint8_t sclk, uint8_t thebyte);
#endif
