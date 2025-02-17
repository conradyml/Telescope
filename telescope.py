import time
import board
import busio
import pwmio

# using adafruit motor hat
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

kit = MotorKit(address=0x60)

pca = PCA9685(board.I2C(),address=0x60)
pca.frequency = 50
servo1 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400,actuation_range=135)

#In astronomy, "telescope azimuth" refers to the horizontal angle of a telescope's pointing direction, measured 
# clockwise from north, while "elevation" refers to the vertical angle of the telescope pointing upwards from the horizon, 
class Position:
	def __init__(self,azimuth,elevation):
		self.azimuth = azimuth
		self.elevation = elevation

	def change_azimuth(self,changeAngle):
		self.azimuth = self.azimuth+changeAngle
		
	def change_elevation(self,changeAngle):
		self.elevation = self.elevation+changeAngle

	def set_azimuth(self,changeAngle):
		self.azimuth = changeAngle
		
	def set_elevation(self,newAngle):
		self.elevation = newAngle
	
	def to_string(self):
		return (f'{{"azimuth":"{self.azimuth}", "elevation":"{self.elevation}"}}')
		


class Telescope:
	def __init__(self,azimuthDegree,elevationDegree):
		self.position = Position(0,0)
		self.focus = 0
		self.azimuth_motor = kit.stepper2
		self.azimuth_steps_per_degree = azimuthDegree
		self.elevation_motor = kit.stepper1
		self.elevation_steps_per_degree = elevationDegree
		self.focus_motor = servo1

	def set_azimuth(self,newAzimuth):

		changeSteps = int(abs(self.position.azimuth-newAzimuth)*self.azimuth_steps_per_degree)
		
		if self.position.azimuth > newAzimuth:
			for i in range(changeSteps):
				self.azimuth_motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
				self.position.change_azimuth(-1/self.azimuth_steps_per_degree)
		else:
			for i in range(changeSteps):
				self.azimuth_motor.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
				self.position.change_azimuth(1/self.azimuth_steps_per_degree)
		
		self.azimuth_motor.release()


	def set_elevation(self,newElevation):
		
		changeSteps = int(abs(self.position.elevation-newElevation)*self.elevation_steps_per_degree)
		if self.position.elevation > newElevation:
			for i in range(changeSteps):
				self.elevation_motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
				self.position.change_elevation(-1/self.elevation_steps_per_degree)
		else:	
			for i in range(changeSteps):
				self.elevation_motor.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
				self.position.change_elevation(1/self.elevation_steps_per_degree)
		
		self.elevation_motor.release()

	def set_focus(self, newFocus):
		# Focus value is expected to be a floating point number between 0 and 1.
			if 0 <= newFocus <= 1
				self.focus_motor.fraction = newFocus
				self.focus = newFocus

			return self.focus

	
# driver function 
#if __name__ == '__main__': 
#	telescope = Telescope(kit.stepper2,50,kit.stepper1,50,None) 
