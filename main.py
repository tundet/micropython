from pyb import Pin, ADC, UART, I2C, DAC
import char_lcd
import time
import math
import binascii
import pyb
from light import lightvalue
print ("kek")

#Define sensors
tempsensor = ADC(Pin('X1'))
motionsensor = Pin('Y12', Pin.IN, Pin.PULL_UP)
beeper = DAC(1)
waterportion = Pin('X11', Pin.OUT_PP)

doortrigger = Pin('Y7', Pin.IN, Pin.PULL_UP)
doortrigger2 = Pin('Y8', Pin.IN, Pin.PULL_UP)

#Define UART bus and I2C bus 
uart = UART(6, 115200)

i2c = I2C(1, I2C.MASTER, baudrate = 9600)
i2c2 = I2C(2, I2C.MASTER, baudrate = 9600)

#Define LCD
d = char_lcd.HD44780(i2c2)

def changetemp(temp):

	#Convert the value the temperature sensor gives into celsius:
	URX = (temp / 4095) * 3.3
	Rx = (URX * 1780) / (3.3 - URX)
	
	if 1922 < Rx <= 2000:
		
		wew = Rx - 1922
		wow = wew / 78
		wiw = 5 * wow
		wuw = 20 + wiw
		decimaltemp = "%.2f" % wuw
		message(decimaltemp)
		
	elif Rx > 1772 and Rx <= 1922:
		
		wew = Rx - 1772
		wow = wew / 150
		wiw = 10 * wow
		wuw = 10 + wiw
		decimaltemp = "%.2f" % wuw
		message(decimaltemp)
	
	elif Rx > 2000 and Rx <= 2080:
		
		wew = Rx - 2000
		wow = wew / 80
		wiw = 5 * wow
		wuw = 25 + wiw
		decimaltemp = "%.2f" % wuw 	
		message(decimaltemp)
		
def message(temp):

	#Creating message
	array = (sensor, lightLevel, temp, doortriggervalue)
	a = str(array)

	sendmessage(a)

def sendmessage(a):

	#Sending message and removing the unneccesary marks.
	a = a+ '\n'
	a = a.replace("(", "")
	a = a.replace(")", "")
	a = a.replace("'", "")
	a = a.replace(" ", "")
	uart.write(bytes(a.encode('ascii')))
	
def keypad () :
	
	#Initial configuration
	i2c2.mem_write(0xFF, 0x20, 0x0C)
	i2c2.mem_write(0xFF, 0x20, 0x00)
	i2c2.mem_write(0x00, 0x20, 0x14)
	
	#Reading (COL1)
	i2c2.mem_write(0xEF, 0x20, 0x00)
	k1 = i2c2.mem_read(1, 0x20, 0x12)
	c1 = k1[0] & 0x2B
	
	#Reading (COL2)
	i2c2.mem_write(0xBF, 0x20, 0x00)
	k2 = i2c2.mem_read(1, 0x20, 0x12)
	c2 = k2[0] & 0x2B
	
	#Reading (COL3)
	i2c2.mem_write(0xFB, 0x20, 0x00)
	k3 = i2c2.mem_read(1, 0x20, 0x12)
	c3 = k3[0] & 0x2B
	
	#Define waterportion value
	wpvalue = waterportion.value()		
	
	#When keypad's number 1 is pressed water flows
	if c1 == 11:
		d.set_line(0)
		d.set_string("WOW!")
		d.set_line(1)
		d.set_string("Water coming")
		wpvalue = waterportion.value(1)
		
	#When no buttons are pressed water flow stops
	elif c1 == 43 and c2 == 43 and c3 == 43:
		d.set_line(0) 
		d.set_string('Press 1 for')
		d.set_line(1)
		d.set_string("water") 
		wpvalue = waterportion.value(0)
	
	else:
		d.set_line(0) 
		d.set_string("You've had")
		d.set_line(1)
		d.set_string("enough")
		wpvalue = waterportion.value(0)
	
	#Print the button that is pressed
	if c1 != 43:
		if c1 == 35:
			print("*")
			pyb.delay(200)
		elif c1 == 41:
			print("7")
			pyb.delay(200)
		elif c1 == 42:
			print("4")
			pyb.delay(200)
		elif c1 == 11:
			print("1")
			pyb.delay(200)
		else:
			print("error")
			pyb.delay(200)
			
	elif c2 != 43:
		if c2 == 35:
			print("0")
			pyb.delay(200)
		elif c2 == 41:
			print("8")
			pyb.delay(200)
		elif c2 == 42:
			print("5")
			pyb.delay(200)
		elif c2 == 11:
			print("2")
			pyb.delay(200)
		else:
			print("error")
		
	elif c3 != 43:
		if c3 == 35:
			print("#")
			pyb.delay(200)
		elif c3 == 41:
			print("9")
			pyb.delay(200)
		elif c3 == 42:
			print("6")
			pyb.delay(200)
		elif c3 == 11:
			print("3")
			pyb.delay(200)
		else:
			print("error")

def beep(beeper):
	if sensor == 0:
		#create a buffer containing a sine-wave
		buf = bytearray(100)
		for i in range(len(buf)):
			buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))
			
		#output the sine-wave at 400hz
		beeper.write_timed(buf, 400 * len(buf), mode = DAC.NORMAL)

#Loop starts
while True:	
	
	#Read motionsensor value
	sensor = (motionsensor.value()) * 10
	
	#Read temperature value
	temp = tempsensor.read()
	
	#Reaad light level value
	lightLevel = lightvalue(i2c) / 10
	
	#Define doortrigger value
	trigger1 = doortrigger.value()
	trigger2 = doortrigger2.value()
	doortriggervalue = 10 * (trigger1 + trigger2)

	keypad()		
	changetemp(temp)
	beep(beeper)
	
