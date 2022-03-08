#include <arduino.h>

void setup() {
  // put your setup code here, to run once:
  SerialUSB.begin(9600);
  pinMode(16, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int i = 1;
  if(digitalRead(16)==LOW){
    SerialUSB.print(i);
    SerialUSB.println(" : Hello World");
    i++;
    // delay(500);
  }

  
}