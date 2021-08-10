#ifndef L298N_h
    #define L298N_h

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
void actuate(long *val, uint8_t pins[2]);

// set a pin to HIGH or LOW
void setPin(uint8_t pin, bool state);

#endif
