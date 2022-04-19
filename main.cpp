#include <Arduino.h>
#include "HID-Project.h"
#include <math.h>



void setup() {
  pinMode(16, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
  pinMode(12, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(18, INPUT);
  Keyboard.begin();
  // Keyboard.release(KEY_P);
  // Keyboard.release(KEY_UP_ARROW);
  SerialUSB.begin(9600);
  // Grenswaarden geluidssensor berekenen
  // int *waarden = getGeluidswaarden();
  // int mean = getGemiddelde(waarden);
  // int deviatie = getDeviatie(waarden);
  // int g1 = mean - deviatie - 50;
  // int g2 = mean + deviatie + 50;
}

int * getGeluidswaarden(){
  int waarden [30];
  int n = sizeof(waarden);
  for(int i=0; i<n-1;i++){
    int val = analogRead(18);
    waarden[i] = val;
    delay(100);
  }
  return waarden;
}

int getGemiddelde(int *w){
    int sum;
    int n = sizeof( w);
    for(int i=0;i<n-1;i++){
        sum += w[i];
    }
    int mean = (int)(sum/n);
    return mean;
}
int getDeviatie(int *w){
    int mean = getGemiddelde(w);
    int n = sizeof(w);
    int sum;
    for(int i=0;i<n-1;i++){
        sum += pow((w[i] - mean),2);
    }
    int sigma = (int) (sqrt(sum/n));
    return sigma;
}

void loop() {
  // Geluidssensor --> P --> dingen oprapen
  // int g1, g2;
  int val = analogRead(18);
  SerialUSB.println (val);
  if(val<520 || val>560){
    // Keyboard.press(KEY_P);
    SerialUSB.println('1');
    delay(100);
    // Keyboard.release(KEY_P);
    // SerialUSB.println(0);
  }
  else{
    SerialUSB.println('0');
    // Keyboard.release(KEY_P);
  }
  // Button op sensor slot 1 --> key up --> Vooruitgaan
  while(digitalRead(14)==LOW){
    SerialUSB.println('2');
  }
  if(digitalRead(14)==LOW){
    
    SerialUSB.println('2');
    // Keyboard.press(KEY_UP_ARROW);
  }
  else{
    SerialUSB.println('3');
  //   // Keyboard.release(KEY_UP_ARROW);
  }
    // see if there's incoming serial data:
  if (SerialUSB.available() > 0) {
    // read the oldest byte in the serial buffer:
    int data = SerialUSB.read();
    // ontvangt als door portal --> vibrator 1 trilt
    if(data ==byte('116')){
        digitalWrite(12, HIGH);
    }
    // delay(100);
    digitalWrite(12, LOW);
    // ontvangt als iets oprapen --> buzzer piept (kort)
    if(data == byte('98')){
      digitalWrite(2, HIGH);
    }
    delay(50);
    digitalWrite(2, LOW);
  };
}
