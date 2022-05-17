#include <arduino.h>
#include <Wire.h>
#include "Segmentdriver.h"
//#include "Ioexpander.h"

Segmentdriver::Segmentdriver(uint8_t addr){
    this->io = new Ioexpander(addr);
}

void Segmentdriver::init(){
    this->io->init();
    this->io->set_conf_reg(0x00);
}

void Segmentdriver::write_value(u_int8_t val_byte){
    switch (val_byte){
    case 0:
        io->set_out_reg(0b01000000);
        break;
    case 1:
        io->set_out_reg(0b01111001);
        break;
    case 2:
        io->set_out_reg(0b00100100); //0x4A
        break;
    case 3:
        io->set_out_reg(0b00110000); //0xB0
        break;
    case 4:
        io->set_out_reg(0b00011001); //0x99
        break;
    case 5:
        io->set_out_reg(0b00010010); //0x92
        break;
    case 6:
        io->set_out_reg(0b00000010); //0x82
        break;
    case 7:
        io->set_out_reg(0b01111000); //0xF8
        break;
    case 8:
        io->set_out_reg(0b00000000); //0x80
        break;
    case 9:
        io->set_out_reg(0b00010000); //0x90
        break;
    case 17:
        io->set_out_reg(0b01000111); //L
        break;
    default:
        io->set_out_reg(0b00000000);
        break;
    }
    
}

