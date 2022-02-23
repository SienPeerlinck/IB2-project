#include <arduino.h>
#include <Wire.h>
#include "Ioexpander.h"

Ioexpander::Ioexpander(uint8_t addr){
    _address = addr;
}

void Ioexpander::init(){
    Wire.begin();
}

void Ioexpander::set_conf_reg(u_int8_t reg_byte){
    Wire.beginTransmission(this->_address);
    Wire.write(0x03);
    Wire.write(reg_byte);
    Wire.endTransmission();
}

void Ioexpander::set_out_reg(u_int8_t reg_byte){
    Wire.beginTransmission(this->_address);
    Wire.write(0x01);
    Wire.write(reg_byte);
    Wire.endTransmission();
}
