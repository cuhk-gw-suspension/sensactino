#include <ADS1X15.h>

ADS1115 ADS(0x48);
long sensorValue = 0;  // variable to store the value coming from the sensor
const uint8_t channel = 0; // ADS1115's analogIn channel
const int nbyte_msg = 7;    // byte length of the msg
const byte header = (byte) '\t';
const byte footer = (byte) '\n';
const char measure = 'r';   // character to receive for print value once. */
const char getInfo = 'i';   // character to receive for printing info of the devcice. */

const char info[] = "";     // infomation about the device.

volatile bool RDY = false;
volatile char cmd;

template <typename T>
void fastSerialPrintln(T value){
  size_t len = sizeof(value);
  byte msg[nbyte_msg] = {};
  msg[0] = header;
  while (Serial.availableForWrite() < nbyte_msg) { ;}

  // parse value to bytes into msg array
  for (int i = 0; i < len; i++) {
      msg[nbyte_msg-2-len+i] = (byte) ((value >> (len-i-1)*8) & 0xFF);
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
  ADS.setGain(1);        // +-4.096 volt
  ADS.setDataRate(5);    // 250Hz

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
    cmd = Serial.read();
    if (cmd == measure)
      fastSerialPrintln(sensorValue);
    if (cmd == getInfo)
      Serial.println(info);
  }
}

void adsReady()
{
  RDY = true;
}

// check if the conversion is ready.
void handleConversion()
{
if (RDY)
  {
    // save the value
    sensorValue = ADS.getValue();
    RDY = false;
  }
}
