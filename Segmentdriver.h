#ifndef Segmentdriver_h
#define Segmentdriver_h
#include <arduino.h>
#include <Wire.h>
#include "Ioexpander.h"

class Segmentdriver {
  public:
    Segmentdriver(u_int8_t addr);
    void init();
    void write_value(u_int8_t val_byte);

  private:
    Ioexpander *io;
};

#endif