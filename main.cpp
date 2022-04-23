//Door foutmelding moest ik adafruit busio installeren als library
//dan moest ik SPI volgens het internet includen, omdat ik nog een andere bepaalde foutmelding kreeg

#include <SPI.h>
#include <Arduino.h>
#include "HID-Project.h"
#include <math.h>
#include "Wire.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_sensor.h>
#include "SparkFun_VCNL4040_Arduino_Library.h"
#include "Ioexpander.h"
#define I2C_ADDRESS 0x3B //led
Ioexpander ioe(I2C_ADDRESS);
Adafruit_MPU6050 mpu;
VCNL4040 proximitySensor;
bool up_gedrukt = false;
bool down_gedrukt = false;
bool right_gedrukt = false;
bool left_gedrukt = false;
bool touch_gedrukt = false;
unsigned long tijd1;
unsigned long vorige_tijd1;
unsigned long delta_tijd1;
unsigned long tijd2;
unsigned long vorige_tijd2;
unsigned long delta_tijd2;
uint8_t data;
bool buzz;
bool i = true;
bool flikkeren = false;
int aantal_keer_60_ms = 0;

void setup() {
  ioe.init();
  ioe.set_conf_reg(0x00);
  ioe.set_out_reg(0x00);

  vorige_tijd1 = millis();
  vorige_tijd2 = millis();
  Wire.begin();

  pinMode(14, INPUT_PULLUP);// sensor slot 1
  pinMode(15, INPUT_PULLUP);//2
  pinMode(16, INPUT_PULLUP);//3
  pinMode(17, INPUT_PULLUP);//4
  pinMode(18, INPUT);       //5
  pinMode(19, INPUT);       //6
  pinMode(24, INPUT);       //7
  pinMode(3, INPUT);        //8
  pinMode(12, OUTPUT);      //vibrator 1
  pinMode(5, OUTPUT);       //vibrator 2
  pinMode(2, OUTPUT);       //gpio buzzer
  pinMode(6, OUTPUT);       //lampjes:
  pinMode(39, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  digitalWrite(6,LOW);
  digitalWrite(39,LOW);
  digitalWrite(8,LOW);
  digitalWrite(9,LOW);
  
  SerialUSB.begin(9600);

  if (proximitySensor.begin() == false)
  {
    Serial.println("Device not found. Please check wiring.");
    while (1); //Freeze!
  }

  while (!Serial){
    delay(10);
    SerialUSB.println("serialUSB not found");
  } 
  if (!mpu.begin()) {
    // SerialUSB.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
      SerialUSB.println("failed");
    }
  }
  if(digitalRead(24)==LOW){
    touch_gedrukt = false;
  } else {
    touch_gedrukt = true;
  }
}

void loop() {



  tijd1 = millis();
  tijd2 = millis();
  delta_tijd1 = tijd1 - vorige_tijd1;
  delta_tijd2 = tijd2 - vorige_tijd2;


  //trillen buzzers 1 voor 1
  if(delta_tijd2 >= 200 && buzz == true){
    buzz = true;
    digitalWrite(12,HIGH);
    digitalWrite(5,LOW);
     //voor led array
  }
  if(delta_tijd2 >= 400 && buzz == true){
    buzz = false;
    digitalWrite(12,LOW);
    digitalWrite(5,LOW);
    digitalWrite(6,LOW);
    digitalWrite(39,LOW);
    digitalWrite(8,LOW);
    digitalWrite(9,LOW);
  }
  
  if(delta_tijd1 >= 60){
    // SerialUSB.println(digitalRead(3)); DEZE DOET HET NIET?


    // PROXIMITY SENSOR:
    unsigned int proxValue = proximitySensor.getProximity();
    SerialUSB.println('p'+ String(proxValue));
    //SerialUSB.println(proxValue);

      // 100 is ongeveer 1 decimeter weg
      //  30 is ongeveer 2 decimeter
      //  10 is ongeveer 3 decimeter
      //   5 is speelafstand

    // XY SENSOR:
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    SerialUSB.println("a"+String(a.acceleration.x-0.43));
    //SerialUSB.println(a.acceleration.x-0.43);

      // 0.43 is horizontaal
      // 10.4 is volledig naar links
      // 9.6  is volledig naar rechts

    vorige_tijd1 = millis();

    aantal_keer_60_ms += 1;
    if(aantal_keer_60_ms == 6){
      i = !i;
      aantal_keer_60_ms = 0;
    }
  }

  // Geluidssensor --> P --> dingen oprapen
  // int g1, g2;
  int val = analogRead(18);
  // SerialUSB.println (val);
  if(val<500 || val>580){

    SerialUSB.println(21);
    delay(100);
  }
  else{
    // Keyboard.release(KEY_P);
  }

  // Button op sensor slot 1 --> key up --> Vooruitgaan
  if(digitalRead(14)==LOW && up_gedrukt == false){ // UP
    SerialUSB.println(11);
    up_gedrukt = true;
  }
  if(digitalRead(14)==HIGH && up_gedrukt == true) {
    SerialUSB.println(12);
    up_gedrukt = false;
  }
  if(digitalRead(15)==LOW && right_gedrukt == false){ // RIGHT
    SerialUSB.println(13);
    right_gedrukt = true;
  }
  if(digitalRead(15)==HIGH && right_gedrukt == true) {
    SerialUSB.println(14);
    right_gedrukt = false;
  }
  if(digitalRead(16)==LOW && down_gedrukt == false){ // DOWN
    SerialUSB.println(15);
    down_gedrukt = true;
  }
  if(digitalRead(16)==HIGH && down_gedrukt == true) {
    SerialUSB.println(16);
    down_gedrukt = false;
  }
  if(digitalRead(17)==LOW && left_gedrukt == false){ // LEFT
    SerialUSB.println(17);
    left_gedrukt = true;
  }
  if(digitalRead(17)==HIGH && left_gedrukt == true) {
    SerialUSB.println(18);
    left_gedrukt = false;
  }
  if(digitalRead(24)==LOW && touch_gedrukt == false){ // LEFT
    SerialUSB.println(19);
    touch_gedrukt = true;
  }
  if(digitalRead(24)==HIGH && touch_gedrukt == true) {
    SerialUSB.println(19);
    touch_gedrukt = false;
  }
  // tone(2,200);
  // delay(400);
  // tone(2,400,300);

    // see if there's incoming serial data:
  if (SerialUSB.available() > 0) {
   
    // !!!
   
    // DE DATA DIE IN PYTHON IS DOORGESTUURD VERANDERD VAN DECIMAAL NAAR UTF8, CONVERSIE KAN JE OP VOLGENDE SITE DOEN:
    // https://onlineutf8tools.com/convert-utf8-to-decimal
   
    
    // read the oldest byte in the serial buffer:
    data = SerialUSB.read();

    // ontvangt als door portal --> vibrator 1 trilt
    if(data == 48){
        tone(2,10000,50);
    }

    if(data == 49){
        vorige_tijd2 = millis();
        buzz = true;
        digitalWrite(12,HIGH);
        digitalWrite(5,HIGH);
        digitalWrite(6,HIGH);
        digitalWrite(39,HIGH);
        digitalWrite(8,HIGH);
        digitalWrite(9,HIGH);
    }

    if(data == 65) {
      ioe.set_out_reg(0xF8); //allemaal aan
      flikkeren = false;
    }
    if(data == 66){
      ioe.set_out_reg(0xF0);
      flikkeren = false;
    }
    if(data == 67){
      ioe.set_out_reg(0xE0);
      flikkeren = false;
    }
    if(data == 68){
      ioe.set_out_reg(0xC0);
      flikkeren = false;
    }
    if(data == 69){
      ioe.set_out_reg(0x80);
      flikkeren = false;
    }
    if(data == 70){
      flikkeren = true;
    }
    if(data == 71){
      ioe.set_out_reg(0x00);
      flikkeren = false;
    }
  };
  if(flikkeren == true){
    if(i == true){
      ioe.set_out_reg(0xF8);
    }else {ioe.set_out_reg(0x00);}
  }
  
}
    
