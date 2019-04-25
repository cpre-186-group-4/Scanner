
import csv
import RPi.GPIO as GPIO
from time import *
import math
from picamera import PiCamera
import IMU
#Sets up the Pi Camera
camera = PiCamera()
#Sets up the GPIO Pins so I can get a read for them
GPIO.setmode(GPIO.BCM)
#Sets up the IMU
IMU.detectIMU()
IMU.initIMU() 

sleepTime = 0.1 #Sets the sleep time so there is a slight delay
lightPin = 0  #Which GPIO Pin the light is connected to 
buttonPin = 0 #Which GPIO Pin the button is connected to 
button = 0  #The output of the button is 1 for pressed or 0 for not | set it to not
pressed = True
count = 0
StartTime = 0
Vectors = [] #Holds the output that i send to the CSV file

#Sets up the GPIO Pins with the exact GPIO Pin
GPIO.setup(lightPin, GPIO.out)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPI.PUD_UP)
GPIO.output(lightPin, False) #Make the light off at the start

#Returns the magnitude
def mag(x, y, z):
	return math.sqrt((x*x)+(y*y)+(z*z))

#Calculates the position and rotations and saves it in a array
def calculate(Vectors, count, T):
	t = time() - T
	#Converts the data to readable data that I can calculate the position from the value
	accX = ((IMU.readACCx() * 0.732) / 1000)
	accY = ((IMU.readACCy() * 0.732) / 1000)
	accZ = ((IMU.readACCz() * 0.732) / 1000)
	#creates the position
	if count >= 1:
		vx = (t * accX)
		vy = (t * accY)
		vz = (t * accZ)
		pz = ((1.0/2.0) * accZ * (t * t))
		py = ((1.0/2.0) * accY * (t * t))
		px = ((1.0/2.0) * accX * (t * t))
		Pitch = math.atan(accX/math.sqrt((accY * accY) + (accZ * accZ)))
		Roll = math.atan(accY/math.sqrt((accX * accX) + (accZ * accZ)))
		Yaw = math.atan(accZ/math.sqrt((accX * accX) + (accY * accY)))
	#adds it to the array
	Vectors.append([px, py, pz, Pitch, Roll, Yaw])

	format(Vectors(len([Vectors])-1)

	#sends it over to be added to the CSV file
	return Vectors

#Formats every value to 2 decimal spots
def format(V):
	for i in range(len(V)):
		V[i] = round(V[i],2)

#Creates the CSV file and outputs all the data
def printVectors(V):
	with open('Positions.csv', mode = 'w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter = ' ')
		for row in Vectors:
			csv_writer.writerow(row)
	csv_file.close()

try:
	StartTime = time() #Intial Time
	while pressed:

		if(GPIO.input(buttonPin) == 0: #Pressed
			button = 1 #Set it to pressed
			camera.start_recording('3D_Scan.h264')#Start recording the video
			sleep(sleepTime)
			if button == 1:
				if(GPIO.input(buttonPin) == 0: #Pressd again
					pressed = false #End the loop
			if button == 1: #Video is still running
				count += 1
				Vectors = calculate(Vectors, count, StartTime) #Calculate the data
			GPIO.output(lightPin, button) #Keeps the light turned on
			sleep(sleepTime)

#After stop the video and close everything
finally:
	printVectors(Vectors)
	GPIO.output(lightPin, false)
	camera.stop_recording()
	GPIO.cleanup()
