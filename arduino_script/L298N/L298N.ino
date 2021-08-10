#include "MyParseNumber.h"
#include "L298N.h"

volatile long value;                // incoming value from pc
const uint8_t dir_pins[2] = {2, 3};        // direction pins

//  1 | 4  | 1 | 1 
// cmd|data|sum|footer
volatile char incomingBytes[8] = {}; // max length 7, min 3 

const char info[64] = "I am an actuator"; //change for individual actuator


void parseBytes(char footer='\n'){
    volatile char c; int i = 0;
    
    do {
        if (Serial.available()){
            c = Serial.read();
            incomingBytes[i] = c;
            i++;
        }
    } while (c != footer);
   
    c = incomingBytes[0];  // change to 1 when multiple device

    if (isupper(c)){
        switch(c){
        case('S'):
            myParseInt_(&value, incomingBytes + 1, footer);
            Serial.println(value);
            break;

        case('M'):
            Serial.println(info);
            break;
        }
    }
}

void setup(){
  Serial.begin(500000);
  while (!Serial) { ;}

  Serial.println("actuator's serial establish");

  pinMode(dir_pins[0], OUTPUT);
  pinMode(dir_pins[1], OUTPUT);

  // use 16bit timer, only pin 9, 10 are available in this mode.
  TCCR1A &= B00111100;
  TCCR1A |= B10000010;
  TCCR1B &= B11100000;
  TCCR1B |= B00010001;
  ICR1 = 0xFFFF;
  pinMode(9, OUTPUT);
}

void loop() {
    // actual code
  if (Serial.available() > 1){
    parseBytes();
    actuate(&value, dir_pins);
  }
}
