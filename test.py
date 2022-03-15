import serial
import time

print('This program allows a user to turn an LED on and off')
print('type H to turn the LED on')
print('type L to turn the LED off')
print('type q to quit')

ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

user_input = 'L'
while user_input != 'q':
    user_input = input('H = on, L = off, q = quit:' )
    byte_command = user_input.encode()
    ser.write(byte_command)  # send a byte
    time.sleep(0.5)  # wait 0.5 seconds

print('q entered. Exiting the program')
ser.close()
