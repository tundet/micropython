import serial
import time
#import rrdtool
import sys
port = serial.Serial('/dev/ttyAMA0', 115200, timeout = 30)

def readmessage():
	while True:
		a = port.readline().decode('ascii')
		a = str(a)
		takaisin = tuple(a.split(","))
		if len(takaisin) > 0:
			print(takaisin)
			time.sleep(5)
		else:
			break;
		purgemessage(str(takaisin))

def purgemessage(takaisin):
	motion = takaisin.split()[0]
	motion = motion.replace(",", "")
	motion = motion.replace("(", "")
	motion = motion.replace("'", "")
       
	light = takaisin.split()[1]
	light = light.replace(",", "")
	light = light.replace("'", "")
	
	temp = takaisin.split()[2]
	temp = temp.replace(",", "")
	temp = temp.replace("\n", "")
	temp = temp.replace(")", "")
	temp = temp.replace("'", "")
	
	adddata(motion, light, temp)
	graphrrd(motion, light, temp)

def createrrd():
	subprocess.call(['rrdtool', 'update', 'test.rrd', '--step', '60'
	,'DS:takaisin:GAUGE:120:-50:50','RRA:MAX:0.5:1:11440'])

def adddata(motion, light, temp):
	subprocess.call(['rrdtool', 'update', 'test.rrd', motion, 
	light, temp])

def graphrrd(motion, ligh, temp):
	subprocess.call(['rrdtool', 'graph', 'test.png', '-w', '1000', '-h',
	'--start', str(int(-86400)), '--end', str(int(now)),
	'DEF:motion=test.rrd:motion.MAX', 'LINE1:motion#ff0000:motion',
	'DEF:light=test.rrd:light.MAX', 'LINE1:light#ff0000:light',
	'DEF:temp=test.rrd:temp.MAX', 'LINE1:temp#ff0000:temp'])

readmessage()


