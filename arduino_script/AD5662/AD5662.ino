#include "MyParseNumber.h"
#include "AD5662.h"

const uint8_t din_pin = 0;
const uint8_t sclk_pin = 1;
const uint8_t sync_pin = 2;
const char info[64] = "I am an actuator"; //change for individual actuator


volatile uint16_t value;                // incoming value from pc

//  1 | 4  | 1 | 1 
// cmd|data|sum|footer
volatile char incomingBytes[8] = {}; // max length 7, min 3 


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
            /* Serial.println(value); */
            break;

        case('I'):
            Serial.println(info);
            break;
        }
    }
}

void setup(){
  Serial.begin(500000);
  while (!Serial) { ;}

  Serial.print(info);
  Serial.println(", port established");
  pinMode(din_pin, OUTPUT);
  pinMode(sclk_pin, OUTPUT);
  pinMode(sync_pin, OUTPUT);

}

void loop() {
    // actual code
  if (Serial.available() > 1){
    parseBytes();
    actuate(&value, din_pin, sclk_pin, sync_pin);
  }
}
