#ifndef DirectAccess_h
    #define DirectAccess_h

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

// initialize provide pin as output
void initOutputPin(uint8_t pin);

// set provide pin as HIGH or LOW
void setOutputPin(uint8_t pin, bool state);

// read digital pin. If HIGH, returns 1. If LOW, returns 0.
bool readPin(uint8_t pin)

#endif
