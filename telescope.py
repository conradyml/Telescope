import time
import board
from busio import I2C

# using adafruit motor hat
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
#from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

i2c = I2C(board.SCL, board.SDA)

#kit = MotorKit(i2c=i2c,address=0x60)
#kit.frequency(50)
pca = PCA9685(board.I2C(),address=0x60)
pca.frequency = 1600
servo1 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400,actuation_range=135)
# setting stepper1 to use M1 and M2 on the hat.
pca.channels[8].duty_cycle = 0xFFFF
pca.channels[13].duty_cycle = 0xFFFF
stepper1 = stepper.StepperMotor(pca.channels[9], pca.channels[10], pca.channels[11], pca.channels[12])

# setting stepper2 to use M3 and M4 on the hat.
pca.channels[7].duty_cycle = 0xFFFF
pca.channels[2].duty_cycle = 0xFFFF
stepper2 = stepper.StepperMotor(pca.channels[4], pca.channels[3], pca.channels[5], pca.channels[6])

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
		self.azimuth_motor = stepper2
		self.azimuth_steps_per_degree = azimuthDegree
		self.elevation_motor = stepper1
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
			if 0 <= newFocus <= 1:
	#			self.focus_motor.fraction = newFocus
				self.focus = newFocus

			return self.focus

	
# driver function 
#if __name__ == '__main__': 
#	telescope = Telescope(kit.stepper2,50,kit.stepper1,50,None) 
