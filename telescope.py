
from a4988 import A4988

motorA = A4988(24,23,22,25)
motorE = A4988(9,10,11,12)
motorF = A4988(5,6,13,26)

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
		self.azimuth_motor = motorA
		self.azimuth_steps_per_degree = azimuthDegree
		self.elevation_motor = motorE
		self.elevation_steps_per_degree = elevationDegree
		self.focus_motor = motorF
		self.azimuth_motor.reset()
		self.elevation_motor.reset()
		
	def set_azimuth(self,newAzimuth):
		changeSteps = int((self.position.azimuth-newAzimuth)*self.azimuth_steps_per_degree)
		self.azimuth_motor.move(changeSteps)
		#self.azimuth_motor.sleep()


	def set_elevation(self,newElevation):
		
		changeSteps = int((self.position.elevation-newElevation)*self.elevation_steps_per_degree)
		self.elevation_motor.move(changeSteps)
		#self.elevation_motor.sleep()

	def set_focus(self, newFocus):
		# Focus value is expected to be a floating point number between 0 and 1.
			if 0 <= newFocus <= 1:
	#			self.focus_motor.fraction = newFocus
				self.focus = newFocus

			return self.focus

	
# driver function 
#if __name__ == '__main__': 
#	telescope = Telescope(kit.stepper2,50,kit.stepper1,50,None) 
