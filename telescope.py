import time
import board
import busio
import pwmio

# using adafruit motor hat
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# using flask_restful 
from flask import Flask, jsonify, request 

kit = MotorKit(address=0x60)

#In astronomy, "telescope azimuth" refers to the horizontal angle of a telescope's pointing direction, measured 
# clockwise from north, while "elevation" refers to the vertical angle of the telescope pointing upwards from the horizon, 
class Position:
	def __init__(self,azimuth,elevation):
		self.azimuth = azimuth
		self.elevation = elevation

	def changeAzimuth(self,changeAngle):
		self.azimuth = self.azimuth+changeAngle
		
	def changeElevation(self,changeAngle):
		self.elevation = self.elevation+changeAngle

	def setAzimuth(self,changeAngle):
		self.azimuth = changeAngle
		
	def setElevation(self,newAngle):
		self.elevation = newAngle

class Telescope:
	def __init__(self,azimuth_motor,azDegree,elevation_motor,elDegree,focus_motor):
		self.position = Position(0,0)
		self.focus = 0
		self.azimuth_motor = azimuth_motor
		self.azimuth_steps_per_degree = azDegree
		self.elevation_motor = elevation_motor
		self.elevation_steps_per_degree = elDegree
		self.focus_motor = focus_motor

	def setAzimuth(self,newAzimuth):
		direction=stepper.FORWARD
		if self.position.azimuth < newAzimuth:
			direction=stepper.BACKWARD

		changeSteps = abs(self.position.azimuth-newAzimuth)*self.azimuth_steps_per_degree
		
		for i in range(changeSteps):
			self.azimuth_motor.onestep(direction=direction, style=stepper.INTERLEAVE)
			self.position.changeAzimuth(1/self.azimuth_steps_per_degree)

	def setElevtion(self,newElevation):
		direction=stepper.FORWARD
		if self.position.elevation < newElevation:
			direction=stepper.BACKWARD

		changeSteps = abs(self.position.elevation-newElevation)*self.elevation_steps_per_degree
		
		for i in range(changeSteps):
			self.elevation_motor.onestep(direction=direction, style=stepper.INTERLEAVE)
			self.position.changeElevation(1/self.elevation_steps_per_degree)
		

telescope = Telescope(kit.stepper2,50,kit.stepper1,50,None)




# creating the flask app 
app = Flask(__name__) 

# making a class for a particular resource 
# other methods include put, delete, etc. 
class Hello(Resource): 

	# corresponds to the GET request. 
	# this function is called whenever there 
	# is a GET request for this resource 
	def get(self): 

		return jsonify({'message': 'hello world'}) 

	# Corresponds to POST request 
	def post(self): 

		data = request.get_json()	 # status code 
		return jsonify({'data': data}), 201

@app.get('/azimuth/')
def azimuth_get():
	return jsonify(telescope.position)

@app.get('/elevation/')
def elevation_get():
	return jsonify(telescope.position)

@app.route('/azimuth/<float:angle>',methods=['PUT','POST'])
def azimuth(angle):
	if request.method == 'PUT':
		angle = telescope.position.azimuth+angle

	telescope.setAzimuth(angle)        
	return jsonify(telescope.position)

@app.route('/elevation/<float:angle>',methods=['PUT','POST'])
def elevation(angle):
	if request.method == 'PUT':
		angle = telescope.position.elevation+angle

	telescope.setElevation(angle)        
	return jsonify(telescope.position)

# another resource to calculate the square of a number 
@app.route('/square/<int:num>')
def get(self, num): 
	return jsonify({'square': num**2}) 

# adding exception response.
class InvalidAPIUsage(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		super().__init__()
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv



@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
	return jsonify(e.to_dict()), e.status_code


# driver function 
if __name__ == '__main__': 

	app.run(debug = True, host="0.0.0.0", port=5000) 
