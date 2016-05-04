import serial
import subprocess
import time
#import rrdtool
import sys
port = serial.Serial('/dev/ttyAMA0', 115200, timeout = 30)

def readmessage():
	while True:
		a = port.readline().decode('ascii').strip()
		if len(a) > 0:
#			print(a)
#			time.sleep(5)

			motion = a.split(",")[0]

			light = a.split(",")[1]

			temp = a.split(",")[2]

			door = a.split(",")[3]
			adddata(motion, light, temp, door)
			graphrrd(motion, light, temp, door)

		else:
			break;

def createrrd():
	subprocess.call(['rrdtool', 'create', 'test.rrd', '--step', '5',
	'DS:motion:GAUGE:120:0:10',
	'DS:light:GAUGE:120:0:40',
	'DS:temp:GAUGE:120:0:30',
	'DS:door:GAUGE:120:0:20',
	'RRA:MAX:0.5:1:120'])

def adddata(motion, light, temp, door):
	subprocess.call(['rrdtool', 'update', 'test.rrd',
	'N:'+ str(motion) + ':'+str(light) + ':'+str(temp) + ':'+str(door)])

def graphrrd(motion, ligh, temp, door):
	subprocess.call(['rrdtool', 'graph', 'test.png', '-w', '1000', '-h', '400',
	'--start', '-400', '--end', 'now',
	'DEF:motion=test.rrd:motion:MAX', 'LINE1:motion#ff1289:motion',
	'DEF:light=test.rrd:light:MAX', 'LINE1:light#ffb400:light',
	'DEF:temp=test.rrd:temp:MAX', 'LINE1:temp#129111:temp',
	'DEF:door=test.rrd:door:MAX', 'LINE1:door#00e3e0:door'])

#createrrd()
readmessage()



