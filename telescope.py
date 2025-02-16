import time
import board
import busio
import pwmio

# using adafruit motor hat
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit(address=0x60)

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
		return (f'{"azimuth":"{self.azimuth}", "elevation":"{self.elevation}"}')
		


class Telescope:
	def __init__(self,azimuth_motor,azDegree,elevation_motor,elDegree,focus_motor):
		self.position = Position(0,0)
		self.focus = 0
		self.azimuth_motor = azimuth_motor
		self.azimuth_steps_per_degree = azDegree
		self.elevation_motor = elevation_motor
		self.elevation_steps_per_degree = elDegree
		self.focus_motor = focus_motor

	def set_azimuth(self,newAzimuth):
		direction=stepper.FORWARD
		if self.position.azimuth < newAzimuth:
			direction=stepper.BACKWARD

		changeSteps = int(abs(self.position.azimuth-newAzimuth)*self.azimuth_steps_per_degree)
		
		for i in range(changeSteps):
			self.azimuth_motor.onestep(direction=direction, style=stepper.INTERLEAVE)
			self.position.change_azimuth(1/self.azimuth_steps_per_degree)

	def set_elevation(self,newElevation):
		
		changeSteps = int(abs(self.position.elevation-newElevation)*self.elevation_steps_per_degree)
		if self.position.elevation < newElevation:
			for i in range(changeSteps):
				self.elevation_motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
				self.position.change_elevation(-1/self.elevation_steps_per_degree)
			
			for i in range(changeSteps):
				self.elevation_motor.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
				self.position.change_elevation(1/self.elevation_steps_per_degree)
		
# driver function 
#if __name__ == '__main__': 
#	telescope = Telescope(kit.stepper2,50,kit.stepper1,50,None) 
