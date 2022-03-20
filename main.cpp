#include <arduino.h>
#include <string.h>

void setup() {
  // put your setup code here, to run once:
  SerialUSB.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  // see if there's incoming serial data:
  if (SerialUSB.available() > 0) {
    // read the oldest byte in the serial buffer:
    int data = SerialUSB.read();
    SerialUSB.print(data);
    if(data == byte(0)){
        digitalWrite(13, HIGH);
    }
    delay(500);
    digitalWrite(13, LOW);
  };
}