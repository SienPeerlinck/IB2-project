#include <arduino.h>
#include <iostream>

void setup() {
	SerialUSB.begin(9600);
}
void loop() {
	if(SerialUSB.available() > 0) {
		char data = SerialUSB.read();
		char str[2];
		str[0] = data;
		str[1] = '\0';
		SerialUSB.print(str);
	}
}