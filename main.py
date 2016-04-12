from pyb import Pin, ADC, UART, I2C
import char_lcd
import time

print ("kek")

adc = ADC(Pin('X1'))
uart = UART(6, 115200)
i2c = I2C(1, I2C.MASTER, baudrate = 9600)
i2clcd = I2C(2, I2C.MASTER, baudrate = 9600)
d = char_lcd.HD44780(i2clcd)

d.set_line(0)
d.set_string("Jotain mukavaa")
d.set_line(1)
d.set_string("Viela mukavampaa")



while True:
	
	
	temp = adc.read()
	i2c.send(0x43, 0x39)
	light = i2c.recv(1, 0x39)

	def changetemp(temp):
		
		URX = (temp / 4095) * 3.3
		Rx = (URX * 1780) / (3.3 - URX)
		
		if 1922 < Rx <= 2000:
			
			wew = Rx - 1922
			wow = wew / 78
			wiw = 5 * wow
			wuw = 20 + wiw
			decimaltemp = "%.2f" % wuw
			print("Lämpötila on: ", decimaltemp)
			message(decimaltemp)
			
		elif Rx > 1772 and Rx <= 1922:
			
			wew = Rx - 1772
			wow = wew / 150
			wiw = 10 * wow
			wuw = 10 + wiw
			decimaltemp = "%.2f" % wuw
			print("Lämpötila on: ", decimaltemp)
			message(decimaltemp)
		
		elif Rx > 2000 and Rx <= 2080:
			
			wew = Rx - 2000
			wow = wew / 80
			wiw = 5 * wow
			wuw = 25 + wiw
			decimaltemp = "%.2f" % wuw
			print("Lämpötila on: ", decimaltemp)
			message(decimaltemp)

	def message(temp):

		alku = (21, 5, 750, 1, light, temp)
		a = str(alku)

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
	
	
	