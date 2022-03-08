import serial
import time
import arduinoComms
# serialports = arduinoComms.listSerialPorts()
# serPort = serialports[0]
ser = serial.Serial('COM4', 9600)
ser.close()
ser.open()


while True:
    data = ser.readline()
    print(data)
