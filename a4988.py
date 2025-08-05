import time
from enum import Enum
import RPi.GPIO as GPIO


# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
FORWARD = 1
REVERSE = 0

class A4988:
	def __init__(self,dir_pin, step_pin,slp_pin,rst_pin):
		self.DIR_PIN=dir_pin
		self.STEP_PIN=step_pin
		self.SLP_PIN=slp_pin
		self.RST_PIN=rst_pin

		GPIO.setup(self.DIR_PIN, GPIO.OUT)
		GPIO.setup(self.STEP_PIN, GPIO.OUT)
		GPIO.setup(self.SLP_PIN, GPIO.OUT)
		GPIO.setup(self.RST_PIN, GPIO.OUT)

	# Function to move the motor
	# speed is steps per second
	def move(self, steps, direction=FORWARD, speed=500):
		if steps<0:
			steps=abs(steps)
			if direction == REVERSE:
				direction = FORWARD
			else:
				direction = REVERSE
		GPIO.output(self.DIR_PIN, direction)
		delay = 1 / speed
		for _ in range(steps):
			GPIO.output(self.STEP_PIN, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(self.STEP_PIN, GPIO.LOW)
			time.sleep(delay)

	def reset(self,hold=1):
		GPIO.output(self.RST_PIN, GPIO.LOW)
		time.sleep(hold)
		GPIO.output(self.RST_PIN, GPIO.HIGH)

	def sleep(self,hold=1):
		GPIO.output(self.SLP_PIN, GPIO.LOW)
		time.sleep(hold)
		GPIO.output(self.SLP_PIN, GPIO.HIGH)



