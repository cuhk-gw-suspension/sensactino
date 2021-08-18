#include "MyParseNumber.h"
#include "AD5662.h"

const uint8_t din_pin = 0;
const uint8_t sclk_pin = 1;
const uint8_t sync_pin = 2;
const char info[64] = "I am an actuator"; //change for individual actuator


long value = 0;                // incoming value from pc

    //   1   | 1 | 4  | 1 |  1 
    // header|cmd|data|sum|footer
const uint8_t sequence_length = 8; // protocol 

//  1 | 4  | 1 | 1 
// cmd|data|sum|footer
char incomingBytes[8] = {}; // max length 7, min 3 
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
        goto skip;
   
    c = incomingBytes[0];  // change to 1 when multiple device
    
    if (isupper(c)){
        switch(c){
        case('S'):
            bytesToLong_(&value, incomingBytes + 1);
            Serial.println(value);
            break;
        case('I'):
            Serial.println(info);
            break;
        }
    }
skip: ;
}

void setup(){
  Serial.begin(500000);
//  while (!Serial) { ;}/

  Serial.print(info);
  Serial.println(", port established");
  pinMode(din_pin, OUTPUT);
  pinMode(sclk_pin, OUTPUT);
  pinMode(sync_pin, OUTPUT);

}

void loop() {
    // actual code
  if (Serial.available() >= sequence_length){
    parseBytes();
    actuate((uint16_t)value, din_pin, sclk_pin, sync_pin);
  }
}
