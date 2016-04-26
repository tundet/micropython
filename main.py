from pyb import Pin, ADC, UART, I2C, DAC
import char_lcd
import time
import math
import binascii
import pyb
print ("kek")

adc = ADC(Pin('X1'))
motionS = Pin('Y12', Pin.IN, Pin.PULL_UP)
beeper = DAC(1)

uart = UART(6, 115200)

i2c = I2C(1, I2C.MASTER, baudrate = 9600)
i2c2 = I2C(2, I2C.MASTER, baudrate = 9600)
<<<<<<< HEAD

=======
>>>>>>> 1d676507d55527271dd42b5396b8a32976e89258
d = char_lcd.HD44780(i2c2)

d.set_line(0) 
d.set_string("Jotain mukavaa") 					#Print out text on first line on the LCD screen
d.set_line(1)
d.set_string("Viela mukavampaa") 				#Print out text on second line on the LCD screen

<<<<<<< HEAD

while True:	
	sensor = motionS.value()
	temp = adc.read()							#Read temperature value
	
=======
while True:	
>>>>>>> 1d676507d55527271dd42b5396b8a32976e89258
	
	i2c.send(0x43, 0x39)						#Send hexadecimal to receiver from sensor 0.
	data0 = i2c.recv(1, 0x39)[0]				#Receive value and convert it to binary number.
	#print(bin(data0)[2:10])	
	chordBits0 = bin(data0)[3:6]				#Convert binary period 2.-4. numbers into decimal numbers.
	chordNumber0 = int(chordBits0, 2)
	chordValue0 = int(16.5*((2 ** chordNumber0) - 1))	#Formula needed to get the value in luxes.
	#print(chordValue0)
	stepValue0 = 2 ** chordNumber0				#Formula needed to get the value in luxes.
	#print (stepValue0)
	stepBits0 = bin(data0)[6:10]				#Convert binary period 5.-8. numbers into decimal numbers.
	stepNumber0 = int(stepBits0, 2)				#Formula needed to get the value in luxes.
	#print (stepNumber0)
	countValue0 = ((chordValue0) + (stepValue0) + (stepNumber0))	#Formula needed to get the value in luxes.
	#print (countValue0)
	i2c.send(0x83, 0x39)						#Send hexadecimal to receiver from sensor 1.
	data1 = i2c.recv(1, 0x39)[0]				#Receive value and convert it to binary number.
	#print(bin(data1)[2:10])
	chordBits1 = bin(data1)[3:6]				#Convert binary period 2.-4. numbers into decimal numbers.
	chordNumber1 = int(chordBits1, 2)
	chordValue1 = int(16.5*((2 ** chordNumber1) - 1))	#Formula needed to get the value in luxes.
	#print(chordValue1)
	stepValue1 = 2 ** chordNumber1				#Formula needed to get the value in luxes.
	#print (stepValue1)
	stepBits1 = bin(data1)[6:10]				#Convert binary period 5.-8. numbers into decimal numbers.
	stepNumber1 = int(stepBits1, 2)				#Formula needed to get the value in luxes.
	#print (stepNumber1)
	countValue1 = ((chordValue1) + (stepValue1) + (stepNumber1))	#Formula needed to get the value in luxes.
	#print (countValue1)
	R = (countValue1)/(countValue0)				#Calculate the ratio of the total values the sensors gave.
	lightLevel = (countValue0) * 0.46 * (math.e ** (-3.13*R))	#Convert the value given by the light sensor into lux. (math.e is a neper number)
<<<<<<< HEAD
	#print(lightLevel)							#Print out the value of the illuminance.
=======
	#print(lightLevel)							#Prin out the value of the illuminance.
>>>>>>> 1d676507d55527271dd42b5396b8a32976e89258
	
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
			print("Temperature is: ", decimaltemp)
			message(decimaltemp)
			
		elif Rx > 1772 and Rx <= 1922:
			
			wew = Rx - 1772
			wow = wew / 150
			wiw = 10 * wow
			wuw = 10 + wiw
			decimaltemp = "%.2f" % wuw
			print("Temperature is: ", decimaltemp)
			message(decimaltemp)
		
		elif Rx > 2000 and Rx <= 2080:
			
			wew = Rx - 2000
			wow = wew / 80
			wiw = 5 * wow
			wuw = 25 + wiw
			decimaltemp = "%.2f" % wuw 	
			print("Temperature is: ", decimaltemp)
			message(decimaltemp)

	def message(temp):
	
		#Creating message.
		array = (sensor, lightLevel, temp)
		a = str(array)

		print(a)
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
		#print(c1)
		#35 = *
		#41 = 7
		#42 = 4
		#11 = 1
		
		#Reading (COL2)
		i2c2.mem_write(0xBF, 0x20, 0x00)
		k2 = i2c2.mem_read(1, 0x20, 0x12)
		c2 = k2[0] & 0x2B
		#print(c2)
		#35 = 0
		#41 = 8
		#42 = 5
		#11 = 2
		
		#Reading (COL3)
		i2c2.mem_write(0xFB, 0x20, 0x00)
		k3 = i2c2.mem_read(1, 0x20, 0x12)
		c3 = k3[0] & 0x2B
		#print(c3)
		#35 = #
		#41 = 9
		#42 = 6
		#11 = 3
		
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
<<<<<<< HEAD
				
	def beep(beeper):
	
		
		
		if sensor == 0:
			print("Disturbance in the force")
			
			#create a buffer containing a sine-wave
			buf = bytearray(100)
			for i in range(len(buf)):
				buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))
			
			#output the sine-wave at 400hz
			beeper.write_timed(buf, 400 * len(buf), mode = DAC.NORMAL)	
		
			
	changetemp(temp)
	#beep(beeper)
	time.sleep(3)
=======
		
			

	#changetemp(temp)
	keypad()
	#time.sleep(5)
>>>>>>> 1d676507d55527271dd42b5396b8a32976e89258
	
	#sleep = 5000
	
<<<<<<< HEAD
	#while sleep > 0:
		#pyb.delay(50)
		#changetemp(temp)
		#keypad()
		#sleep = sleep-50
	
=======
>>>>>>> 1d676507d55527271dd42b5396b8a32976e89258
