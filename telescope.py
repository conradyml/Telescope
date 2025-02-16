import time
import board
import busio
import pwmio

# using adafruit motor hat
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

# using flask_restful 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 

kit = MotorKit(address=0x60)

# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 

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

class stepperMotor(Resource):
	def __init__(self, path):
		Resource.__init__(self, path)
		#self.stepper_motor = stepm
		self.stepper_motor = kit.stepper1
		#self.steps_per_degree=steps
		self.steps_per_degree=50
		self.currentAngle = 0

	def get(self):

		return jsonify({'angle': self.currentAngle})

	def put(self):

		data = request.get_jason()

		if 'angle' not in data:
			raise InvalidAPIUsage("angle data is missing from payload!", status_code=404)

		newAngle = data['angle']
		direction=stepper.FORWARD
		if newAngle < self.currentAngle:
			direction = stepper.BACKWARD

		changeSteps = abs(currentAngle-newAngle)*self.steps_per_degree

		for i in range(changeSteps):
			self.stepper_motor(direction=direction, style=stepper.INTERLEAVE)

		self.currentAngle = newAngle
		return jsonify({'angle': self.currentAngle})


# another resource to calculate the square of a number 
class Square(Resource): 

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


# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/square/<int:num>') 
api.add_resource(stepperMotor, '/azimuth')

@api.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
	return jsonify(e.to_dict()), e.status_code


# driver function 
if __name__ == '__main__': 

	app.run(debug = True) 
