
from a4988 import A4988
import RPi.GPIO

motorA = A4988(24,23,22,25)
motorE = A4988(9,10,11,12)
motorF = A4988(5,6,13,26)




#In astronomy, "telescope azimuth" refers to the horizontal angle of a telescope's pointing direction, measured 
# clockwise from north, while "elevation" refers to the vertical angle of the telescope pointing upwards from the horizon, 
class Position:
	def __init__(self,azimuth,elevation):
		self.azimuth = azimuth
		self.elevation = elevation

	def __eq__(self, other):
        # Check if 'other' is an instance of the same class
		if not isinstance(other, Position):
			return NotImplemented  # Or raise TypeError if you prefer strict type checking

        # Define your equality logic here
        # For example, compare attributes
		return self.azimuth == other.azimuth and self.elevation == other.elevation


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
	def __init__(self,azimuthDegree=50,elevationDegree=40):
		self.position = Position(0,0)
		self.next_position = Position(0,0)
		self.focus = 0
		self.state = 'AWAKE'
		self.azimuth_motor = motorA
		self.azimuth_steps_per_degree = azimuthDegree
		self.elevation_motor = motorE
		self.elevation_steps_per_degree = elevationDegree
		self.focus_motor = motorF
	
		
	def set_azimuth(self,newAzimuth):
		self.next_position.set_azimuth(newAzimuth)
		changeSteps = int((newAzimuth-self.position.azimuth)*self.azimuth_steps_per_degree)
		self.azimuth_motor.move(changeSteps, callback=self.set_az_position_steps)
		#self.azimuth_motor.sleep()

	def set_az_position_steps(self,steps):
		changeAngle = steps/self.azimuth_steps_per_degree
		self.position.change_azimuth(changeAngle)

	def set_elevation(self,newElevation):
		self.next_position.set_elevation(newElevation)
		changeSteps = int((newElevation-self.position.elevation)*self.elevation_steps_per_degree)
		self.elevation_motor.move(changeSteps, callback=self.set_el_position_steps)
		#self.elevation_motor.sleep()

	def set_el_position_steps(self,steps):
		changeAngle = steps/self.elevation_steps_per_degree
		self.position.change_elevation(changeAngle)

	def set_focus(self, newFocus):
		# Focus value is expected to be a floating point number between 0 and 1.
			if 0 <= newFocus <= 1:
	#			self.focus_motor.fraction = newFocus
				self.focus = newFocus
			return self.focus

	def sleep(self):
		self.azimuth_motor.stop()
		self.elevation_motor.stop()
		self.focus_motor.stop()
		self.azimuth_motor.sleep()
		self.elevation_motor.sleep()
		self.focus_motor.sleep()
		self.state="ASLEEP"
	
	def wake(self):
		self.azimuth_motor.reset()
		self.elevation_motor.reset()
		self.focus_motor.reset()
		self.state="AWAKE"
	
	def get_status(self):
		return (f'{{ "Position":{self.position.to_string()}, "Moving_To":{self.next_position.to_string()}, "focus":"{self.focus}"", "state":"{self.state}"}}')
	
	def check_position(self):
		if self.position == self.next_position:
			return self.get_status()
		elif self.azimuth_motor.is_moving() or self.elevation_motor.is_moving():
			return self.get_status()
		else:
			self.next_position = self.position
		return self.get_status()

	
	@staticmethod
	def shutdown():
		RPi.GPIO.cleanup()

	
# driver function 
#if __name__ == '__main__': 
#	telescope = Telescope(kit.stepper2,50,kit.stepper1,50,None) 
