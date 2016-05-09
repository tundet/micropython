
from pyb import Pin, ADC, UART, I2C, DAC
import char_lcd
import time
import math
import binascii
import pyb

i2c = I2C(1, I2C.MASTER, baudrate = 9600)

def lightvalue(i2c):
	#Send hexadecimal to receiver from sensor 0.
	i2c.send(0x43, 0x39)
	
	#Receive value and convert it to binary number.
	data0 = i2c.recv(1, 0x39)[0]				
	
	#Convert binary period 2.-4. numbers into decimal numbers.
	chordBits0 = bin(data0)[3:6]				
	chordNumber0 = int(chordBits0, 2)
	
	#Formula needed to get the value in luxes.
	chordValue0 = int(16.5*((2 ** chordNumber0) - 1))	
	
	#Formula needed to get the value in luxes.
	stepValue0 = 2 ** chordNumber0				
	
	#Convert binary period 5.-8. numbers into decimal numbers.
	#Formula needed to get the value in luxes.
	stepBits0 = bin(data0)[6:10]				
	stepNumber0 = int(stepBits0, 2)				
	
	#Formula needed to get the value in luxes.
	countValue0 = ((chordValue0) + (stepValue0) + (stepNumber0))	
	
	#Send hexadecimal to receiver from sensor 1.
	#Receive value and convert it to binary number.
	i2c.send(0x83, 0x39)						
	data1 = i2c.recv(1, 0x39)[0]				
	
	#Convert binary period 2.-4. numbers into decimal numbers.
	chordBits1 = bin(data1)[3:6]				
	chordNumber1 = int(chordBits1, 2)
	
	#Formula needed to get the value in luxes.
	chordValue1 = int(16.5*((2 ** chordNumber1) - 1))	
	
	#Formula needed to get the value in luxes.
	stepValue1 = 2 ** chordNumber1				
	
	#Convert binary period 5.-8. numbers into decimal numbers.
	#Formula needed to get the value in luxes.
	stepBits1 = bin(data1)[6:10]				
	stepNumber1 = int(stepBits1, 2)				
	
	#Formula needed to get the value in luxes.
	countValue1 = ((chordValue1) + (stepValue1) + (stepNumber1))	
	
	#Calculate the ratio of the total values the sensors gave.
	R = (countValue1)/(countValue0)	

	#Convert the value given by the light sensor into lux. (math.e is a neper number)
	lightLevel = (countValue0) * 0.46 * (math.e ** (-3.13*R))
	return lightLevel