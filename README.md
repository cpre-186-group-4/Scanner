# Scanner
A respository that correlates with the Raspberry Pi 0 and Berry IMU v3 to calculate the position and the rotation of the axis'.
# Scanner Overview
The goal of this project within this repository is to work with the Raspberry Pi 0 (Can be any Pi we choose the 0) and the Berry IMU v3
to take a video of an object, calculate the position and rotation of the Raspberry Pi 0, and then display this information on a CSV
file and save it in a certain location so it can be transferred to our code which finds points from the video and then puts them together 
to get a 3D scan of the object. We built this for our Computer Engineering class at Iowa State University.

The jobs for this program are these:
  * Set up the Raspberry Pi 0, Berry IMU v3, and the Pi Camera
  * Implement our Txt file that deletes old files 
  * Work with buttons and LED lights on the Raspberry Pi
  * Take a video after the button has been pressed
  * Make sure it is not overriding exsisting files
  * Calculate the position and roatation after button has been pressed
  * Turn on LED light while recording
  * Shutdown program when the button is pressed again
  * Print all the data onto a CSV file at the end
