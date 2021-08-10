#include "MyParseNumber.h"

volatile long value;      // incoming value from pc
volatile bool dir;        // direction

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
            break;

        case('M'):
            Serial.println(info);
            break;
        }
    }
}

void setup(){
  Serial.begin(500000);
  while (!Serial) {;}
}

void loop() {
    // actual code
  if (Serial.available() > 1){
    parseBytes();
    actuacte(&value);
  }
}
