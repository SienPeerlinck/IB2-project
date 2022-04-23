#ifndef Ioexpander_h
#define Ioexpander_h

#include <arduino.h>
#include <Wire.h>

class Ioexpander{
  public:
    Ioexpander(uint8_t addr);
    void init();
    void set_conf_reg(u_int8_t reg_byte);
    void set_out_reg(u_int8_t reg_byte);
  private:
    uint8_t _address;
};

#endif