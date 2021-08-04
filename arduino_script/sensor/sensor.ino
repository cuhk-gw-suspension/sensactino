#include <ADS1X15.h>

ADS1115 ADS(0x48);
//int sensorPin = A0;    // select the input pin for the potentiometer
long sensorValue = 0;  // variable to store the value coming from the sensor
const uint8_t channel = 0;
const int nbyte_msg = 7;    // byte length of the msg
const byte header = (byte) '\t';
const byte footer = (byte) '\n';
const char cmd = 'o';   // character to receive for print once.

volatile bool RDY = false;


template <typename T>
void fastSerialPrintln(T value){
  size_t len = sizeof(value);
  byte msg[nbyte_msg] = {};
  msg[0] = header;
  while (Serial.availableForWrite() < nbyte_msg) { ;}

  // parse value to bytes in msg array
  for (int i = nbyte_msg - 2 - len; i < nbyte_msg - 2; i++) {
      msg[i] = (byte) ((value >> (len-i-1)*8) & 0xFF);
  }
  
  // checksum using XOR
  byte checksum = msg[1];
  for (int i = 2; i < nbyte_msg-2; i++)
    checksum ^= msg[i];
  
  msg[nbyte_msg-2] = checksum;
  msg[nbyte_msg-1] = footer;
  Serial.write(msg, nbyte_msg);
}

void setup() {
  Serial.begin(500000);
  while (!Serial) {;}

  ADS.begin();
  ADS.setGain(0);        // +-6.144 volt
  ADS.setDataRate(7);    // fast

  // SET ALERT RDY PIN
  ADS.setComparatorThresholdHigh(0x8000);
  ADS.setComparatorThresholdLow(0x0000);
  ADS.setComparatorQueConvert(0);

  // SET INTERRUPT HANDLER TO CATCH CONVERSION READY
  pinMode(2, INPUT_PULLUP);

  ADS.setMode(0);        // continuous mode
  ADS.readADC(channel);     // trigger first read
}

void loop() {
//    sensorValue = analogRead(sensorPin);
  if (digitalRead(2))
    adsReady();  
  handleConversion();
  delayMicroseconds(10);
  
  if (Serial.available() > 0){
    if (Serial.read() == cmd)
      fastSerialPrintln(sensorValue);
  }
}

void adsReady()
{
  RDY = true;
}

void handleConversion()
{
if (RDY)
  {
    // save the value
    sensorValue = ADS.getValue();
    RDY = false;
  }
}
