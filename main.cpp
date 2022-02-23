#include <Arduino.h>
#include "Segmentdriver.h"

Segmentdriver seg1(0x3A);
Segmentdriver seg2(0x39);

uint8_t var1 = 0;
uint8_t var2 = 0;

void setup(){
  seg1.init();
  seg2.init();
}

void loop(){
  seg1.write_value(var1);
  seg2.write_value(var2);
  delay(500);
  var2++;
  if (var2 > 9){
    var2=0;
    var1++;
    if (var1 > 9){
      var1=0;
      var2=0;
    }
  }
}
