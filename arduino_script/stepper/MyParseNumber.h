#ifndef MyParseNumber_h
    #define MyParseNumber_h

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

void myParseInt_(long *pos, char *number, char delimiter);
/* long myParseInt(); */

/* void bytesToLong_(long *pos, char *number, char delimiter); */

#endif
