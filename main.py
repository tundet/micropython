from pyb import Pin, ADC, UART, I2C
import char_lcd
import time
import math
import binascii

print ("kek")

adc = ADC(Pin('X1'))
uart = UART(6, 115200)
i2c = I2C(1, I2C.MASTER, baudrate = 9600)
i2clcd = I2C(2, I2C.MASTER, baudrate = 9600)
d = char_lcd.HD44780(i2clcd)

d.set_line(0) 
d.set_string("Jotain mukavaa") 					#Print out text on first line on the LCD screen
d.set_line(1)
d.set_string("Viela mukavampaa") 				#Print out text on second line on the LCD screen



while True:
	
	
	temp = adc.read()							#Read temperature value

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
	chordBits1 = bin(data1)[3:6]				Convert binary period 2.-4. numbers into decimal numbers.
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
	print(lightLevel)							#Prin out the value of the illuminance.

	
	def changetemp(temp):
		
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

		array = (21, 5, 750, 1, lightLevel, temp)
		a = str(array)

		print(a)
		sendmessage(a)

	def sendmessage(a):	
		a = a+ '\n'
		a = a.replace("(", "")
		a = a.replace(")", "")
		a = a.replace("'", "")
		a = a.replace(" ", "")
		uart.write(bytes(a.encode('ascii')))
		



	changetemp(temp)
	time.sleep(5)
	
	
	

