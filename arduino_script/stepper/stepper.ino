#include "MyStepper.h"
#include "MyParseNumber.h"

volatile long pos;      // target aboslute position
volatile long disp;     // target relative position

Stepper stepper1(2, 3); //init pul pin=2, dir pin=3

void parseBytes(char footer='\n'){
    //   1   | 1 | 4  | 1 
    // device|cmd|data|footer
    char incomingBytes[8] = {}; // max length 7, min 3 
    volatile char c; int i = 0;
    
    do {
        if (Serial.available()){
            c = Serial.read();
            incomingBytes[i] = c;
            i++;
        }
    } while (c != footer);
   
    /* char c = Serial.read(); */
    c = incomingBytes[0];  // change to 1 when multiple device

    if (isupper(c)){
        switch(c){
//        case('R'):
//            /* while( Serial.read() != footer) {} */
//            Serial.println("reseting");
//            stepper1.sweep(10, 12); // limit switch pins: 10, 12
//            break;
        case('S'):
            myParseInt_(&disp, incomingBytes + 1, footer);
            pos += disp;
            /* stepper1.moveTo(pos); */
            break;

        case('M'):
            /* pos = myParseInt(); */
            myParseInt_(&pos, incomingBytes + 1, footer);
            stepper1.moveTo(pos);
//            Serial.println(pos);
            break;
        }
    }
}

void setup() {
    Serial.begin(500000);
    
    // caution, delay under 3 us is inaccurate. 
    stepper1.setSpeed(100000); // number of steps per sec.

    Serial.println("serial established");
}

void loop() {
    // actual code
    if (Serial.available() > 1){
        parseBytes();
    }
    
    /* if (readPin(10) &&readPin(12)) */
        stepper1.run(); 
}
