# IB2-project

main.cpp in visual studio code openen.

In python volgende aanpassen (te weinig veranderingen om volledige code door te sturen):

import serial

ser = serial.Serial('COM4', 9600)

ser.close()

ser.open()

Dit staat helemaal vanboven, bij de imports

Bij level overgang, juist boven de else (ong.lijn 918, 919):

ser.write(7)  

print(ser.read())

Python verstuurt een byte naar de dramco, dramco leest die en stuurt die terug, door de print-functie kan je die lezen in python. 
Merk op dat als je een int verstuurd, je altijd 0 terugkrijgt (daarmee dat er in de cpp-file 0 staat), als je de byte encodeerd ("7".encode('utf-8')), krijg je een ander random getal terug. Dit moeten we nog uitzoeken.
