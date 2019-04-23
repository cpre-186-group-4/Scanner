
import csv
import RPi.GPIO as GPIO
from time import *
import math
#from picamera import PiCamera
import IMU

#camera = PiCamera()
GPIO.setmode(GPIO.BCM)

sleepTime = 0.1
lightPin = 0
buttonPin = 0
button = 0
pressed = True
count = 0
StartTime = 0
Vectors = []
IMU.detectIMU()
IMU.initIMU()
#GPIO.setup(lightPin, GPIO.out)
#GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPI.PUD_UP)
#GPIO.output(lightPin, False)

def mag(x, y, z):
	return math.sqrt((x*x)+(y*y)+(z*z))

def calculate(Vectors, count, T):
	t = time() - T
	accX = ((IMU.readACCx() * 0.732) / 1000)
	accY = ((IMU.readACCy() * 0.732) / 1000)
	accZ = ((IMU.readACCz() * 0.732) / 1000)
	if count >= 1:
		vx = (t * accX)
		vy = (t * accY)
		vz = (t * accZ)
		pz = ((1.0/2.0) * accZ * (t * t))
		py = ((1.0/2.0) * accY * (t * t))
		px = ((1.0/2.0) * accX * (t * t))
	degrees = math.atan2(accY, accX) * (180/(math.pi))
	Vectors.append([px, py, pz, degrees])
	addVector(Vectors)

def addVector(V):
	with open('Positions.csv', mode = 'w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter = ' ')
		for row in Vectors:
			csv_writer.writerow(row)

try:
	StartTime = time()
	while count < 100:
#		print("Start Time: %.2f" % StartTime)
#		if(GPIO.input(buttonPin) == 0:
#			button = 0
#			camera.start_recording('video.h264')
#			sleep(sleepTime)
#			if button == 1:
#				if(GPIO.input(buttonPin) == 0:
#					pressed = false
#			if button == 1:
		count += 1
		calculate(Vectors, count, StartTime)
#			GPIO.output(lightPin, button)
		sleep(sleepTime)

finally:
	print("finished")
#	GPIO.output(lightPin, false)
#	camera.stop_recording()
#	GPIO.cleanup()
