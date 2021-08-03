#include <ADS1X15.h>

ADS1115 ADS(0x48);
//int sensorPin = A0;    // select the input pin for the potentiometer
long sensorValue = 0;  // variable to store the value coming from the sensor
const uint8_t channel = 0;

volatile bool RDY = false;

template <typename T>
void fastSerialPrintln(T value){
  size_t len = sizeof(value);
  byte msg[len] = {};
  
  
  if(Serial.availableForWrite() > len+1) {
    for (int i = 0; i < len; i++) {
      msg[i] = (byte) ((value >> (len-i-1)*8) & 0xFF);
    }
  }
  Serial.write(msg, len);

  byte checksum = msg[0];
  // checksum using XOR
  for (int i = 1; i < len; i++)
    checksum ^= msg[i];
  Serial.write(checksum);
  Serial.write('\n');
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
    fastSerialPrintln(sensorValue);
    RDY = false;
  }
}
