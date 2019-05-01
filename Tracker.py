#!/usr/bin/python
import os
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
lightPin = 20  #Which GPIO Pin the light is connected to 
buttonPin = 26 #Which GPIO Pin the button is connected to 
button = 0  #The output of the button is 1 for pressed or 0 for not | set it to not
pressed = False
count = 0
StartTime = 0
Vectors = [] #Holds the output that i send to the CSV file

num = 0
while true:
	        name_of_folder = "Scan" + str(num) #Adds a different number so there are no repeats
		if os.path.isfile(name_of_folder): #Checks to see if that exact file exsists already
	       		num+=1
	        else:
	       		break #Breaks the loop because that file with the number doesn't exisit yet
os.mkdir("~/Scans/" + name_of_folder)
Save_Path =  "../Scans/" + name_of_folder + "/" #Tells the code the exact spot it needs to be saved
os.system("chmod u+x ~/Scanner/Commands.txt; /Users/haileylucas/Documents/Command.txt")

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
	#creates the position and rotation
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
	
	#foramts the values in the array
	format(Vectors(len([Vectors])-1))

	#Updates the vectors array
	return Vectors

#Formats every value to 2 decimal spots
def format(V):
	for i in range(len(V)):
		V[i] = round(V[i],2)

#Creates the unique CSV file and outputs all the data
def printVectors(V):
	num = 0
	
	with open('Positions.csv', mode = 'w') as csv_file: #Creates new files that don't exist by adding numbers
		csv_writer = csv.writer(csv_file, delimiter = ' ')
		for row in Vectors:
			csv_writer.writerow(row)
	csv_file.close()

if __name__ == '__main__':
	try:
		StartTime = time() #Intial Time
	        while pressed == False: #Intialized as False
	       		if GPIO.input(buttonPin) == 0: #Pressed
	       			button == 1 #Set button to pressed
	       			num = 0
	       			camera.start_recording("3D_Scan.h264")#Start recording the video
	       			sleep(sleepTime)
	       			pressed = True
	        while pressed:
	       		if GPIO.input(buttonPin) == 0: #Pressd again
					pressed = false #End the loop
			if button == 1: #Video is still running
					count += 1
					Vectors = calculate(Vectors, count, StartTime) #Calculate the data
			GPIO.output(lightPin, button) #Keeps the light turned on
			sleep(sleepTime)

#		while pressed:
#			if GPIO.input(buttonPin) == 0: #Pressed
#				button = 1 #Set it to pressed
#				camera.start_recording('3D_Scan.h264')#Start recording the video
#				sleep(sleepTime)
#				if button == 1:
#					if(GPIO.input(buttonPin) == 0: #Pressd again
#						pressed = false #End the loop
#				if button == 1: #Video is still running
#					count += 1
#					Vectors = calculate(Vectors, count, StartTime) #Calculate the data
#				GPIO.output(lightPin, button) #Keeps the light turned on
#				sleep(sleepTime)

	#After button is pressed again, stop the video and close everything
	finally:
		printVectors(Vectors)
		GPIO.output(lightPin, false)
		camera.stop_recording()
		GPIO.cleanup()
