#include "MyStepper.h"
#include "MyParseNumber.h"

const char info[64] = "I am the stepper"; 

Stepper stepper1(2, 3); //init pul pin=2, dir pin=3

//   1   | 1 | 4  | 1 |  1 
// header|cmd|data|sum|footer
const uint8_t sequence_length = 8; // protocol 
//  1 | 4  | 1 |  1 
// cmd|data|sum|footer
volatile char incomingBytes[8] = {}; 
// #dont know if null byte termination is needed,
// so array-size is 8 to be safe.
long pos;      // target aboslute position
long disp;     // target relative position


void parseBytes(char header='\t', char footer='\n'){
    volatile char c;
    
    // start only when header is read.
    while (Serial.read() != header) { ;}
    // wait for following bytes, if needed.
    while (Serial.available() < 7) { ;}

    for (int i = 0; i < 7; i++) {
        incomingBytes[i] = Serial.read();
    }
    
    // checksum
    c = incomingBytes[0];
    for (int i = 1; i < 6; i++) 
        c ^= incomingBytes[i];
    // handle invalid sequence.
    if (incomingBytes[6] != footer or c != '\0')
        goto skip;
   
    c = incomingBytes[0]; 
    if (isupper(c)){
        switch(c){
        case('R'):
            Serial.println("reseting");
            stepper1.reset(4); // enable_pin = 4, grounded = enabled
            break;
        case('S'):
            bytesToLong_(&disp, incomingBytes + 1);
            pos += disp;
            stepper1.moveTo(pos);
            break;
        case('M'):
            bytesToLong_(&pos, incomingBytes + 1);
            stepper1.moveTo(pos);
//            Serial.println(pos);
            break;
        case('I'):
            Serial.println(info);
            break;
        }
    }
skip: ;
}

void setup() {
    Serial.begin(500000);
    
    // caution, delay under 3 us is inaccurate. 
    stepper1.setSpeed(50000); // number of steps per sec.
    Serial.print(info);//
    Serial.println(", port established");
}

void loop() {
    // actual code
    if (Serial.available() >= sequence_length){
        parseBytes();
    }
    stepper1.run(); 
}
