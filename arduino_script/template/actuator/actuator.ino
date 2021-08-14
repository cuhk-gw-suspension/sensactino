#include "MyParseNumber.h"

const char info[64] = "I am an actuator"; //change for individual actuator

volatile long value;      // incoming value from pc
volatile bool dir;        // direction
//   1   | 1 | 4  | 1 |  1 
// header|cmd|data|sum|footer
const uint8_t sequence_length = 8; // protocol 
//  1 | 4  | 1 | 1 
// cmd|data|sum|footer
volatile char incomingBytes[8] = {}; // max length 7, min 3 
// #dont know if null byte termination is needed,
// so array-size is 8 to be safe.

void parseBytes(char header='\t', char footer='\n'){
    volatile char c;
    // start only when header is read.
    while (Serial.read() != header) { ;}
    // wait for following bytes, if needed.
    while (Serial.available() < 7) { ;}
    // read bytes
    for (int i = 0; i < 7; i++) 
        incomingBytes[i] = Serial.read();
    // checksum
    c = incomingBytes[0];
    for (int i = 1; i < 6; i++) 
        c ^= incomingBytes[i];
    // handle invalid sequence.
    if (incomingBytes[6] != footer or c != '\0')
        goto run;
   
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
  while (!Serial) {;}
}

void loop() {
run:
  if (Serial.available() > 1){
    parseBytes();
    actuacte(&value);  // define an custom actuate function for actuator.
  }
}
