import serial
import subprocess
import time
#import rrdtool
import sys
port = serial.Serial('/dev/ttyAMA0', 115200, timeout = 30)

def readmessage():
	while True:
		a = port.readline().decode('ascii').strip()
		print(a)
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
	temp = temp.replace(")", "")
	temp = temp.replace("'", "")
	
	adddata(motion, light, temp)
	#graphrrd(motion, light, temp)

def createrrd():
	subprocess.call(['rrdtool', 'create', 'test.rrd', '--step', '5',
	'DS:motion:GAUGE:120:0:1',
	'DS:light:GAUGE:120:0:400',
	'DS:temp:GAUGE:120:0:30',
	'RRA:MAX:0.5:1:120'])

def adddata(motion, light, temp):
	subprocess.call(['rrdtool', 'update', 'test.rrd',
	'N:'+ motion + ':'+ light + ':'+ temp])

def graphrrd(motion, ligh, temp):
	subprocess.call(['rrdtool', 'graph', 'test.png', '-w', '1000', '-h', '400',
	'--start', str(int(-86400)), '--end', str(int(now)),
	'DEF:motion=test.rrd:motion:MAX', 'LINE1:motion#ff1289:motion',
	'DEF:light=test.rrd:light:MAX', 'LINE1:light#008003:light',
	'DEF:temp=test.rrd:temp:MAX', 'LINE1:temp#129111:temp'])

createrrd()
readmessage()


