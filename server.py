
from telescope import Telescope

telescope = Telescope(50,50)

# using flask_restful 
from flask import Flask, jsonify, request 


# creating the flask app 
app = Flask(__name__) 

# making a class for a particular resource 
# other methods include put, delete, etc. 
@app.get('/')
def  hello_world():
	PAGE = """\
	<html>
	<head>
	<title>Telescope</title>
	</head>
	<body>
	<h1>Hello, World!</h1>
	</body>
	</html>
	"""
	return PAGE.encode('utf-8')
	
@app.get('/azimuth/')
def azimuth_get():
	return jsonify(telescope.position.to_string())

@app.get('/elevation/')
def elevation_get():
	return jsonify(telescope.position.to_string())

@app.get('/focus/')
def focus_get():
	return jsonify(telescope.focus)


@app.route('/azimuth/<angle>',methods=['PUT','POST'])
def azimuth(angle):
	angle = float(angle)
	if request.method == 'PUT':
		angle = telescope.position.azimuth+angle

	telescope.set_azimuth(angle)        
	return jsonify(telescope.position.to_string())

@app.route('/elevation/<angle>',methods=['PUT','POST'])
def elevation(angle):
	angle = float(angle)
	if request.method == 'PUT':
		angle = telescope.position.elevation+angle

	telescope.set_elevation(angle)        
	return jsonify(telescope.position.to_string())

@app.route('/focus/<value>',methods=['PUT','POST'])
def focus(value):
	angle = float(value)
	if request.method == 'PUT':
		value = telescope.focus+value

	telescope.set_focus(value)        
	return jsonify(telescope.focus)



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
