import time
import threading
import RPi.GPIO as GPIO


# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
FORWARD = 1
REVERSE = 0

def default_callback(message):
	print (f'Callback: {message}')	

class A4988:
	def __init__(self,dir_pin, step_pin,slp_pin,rst_pin):
		self.DIR_PIN=dir_pin
		self.STEP_PIN=step_pin
		self.SLP_PIN=slp_pin
		self.RST_PIN=rst_pin
		self.thread = None
		self.interrupt = threading.Event()
		
		GPIO.setup(self.DIR_PIN, GPIO.OUT)
		GPIO.setup(self.STEP_PIN, GPIO.OUT)
		GPIO.setup(self.SLP_PIN, GPIO.OUT)
		GPIO.setup(self.RST_PIN, GPIO.OUT)
		self.reset()
		self.sleep()

	# Function to move the motor
	# speed is steps per second
	def move(self, steps, direction=FORWARD, speed=500, callback=default_callback, callback_interval=50):
		if steps<0:
			steps=abs(steps)
			if direction == REVERSE:
				direction = FORWARD
			else:
				direction = REVERSE
		self.thread = threading.Thread(target=self.move_threaded, args=(steps,direction,speed,callback, callback_interval))
		#return count

	def move_threaded(self, steps, direction, speed, callback, callback_interval):
		count=0
		if self.thread is not None and self.thread.is_alive():
			print("Thread is running")
			self.interrupt.set()
			print("Thread Interrupted.")
			self.thread.join()
			self.interrupt.clear()
			print ("Interrupt Cleared.")
		while not self.interrupt.is_set() and count < abs(steps):
			print("Enter While 1")
			GPIO.output(self.DIR_PIN, direction)
			delay = 1 / speed
			for _ in range(steps):
				print("Enter For 1")
				GPIO.output(self.STEP_PIN, GPIO.HIGH)
				time.sleep(delay)
				GPIO.output(self.STEP_PIN, GPIO.LOW)
				time.sleep(delay)
				count+=1
				if (count % callback_interval) ==0:
					callback(callback_interval)
		callback(count % callback_interval)

	def reset(self,hold=1):
		GPIO.output(self.RST_PIN, GPIO.LOW)
		time.sleep(hold)
		GPIO.output(self.RST_PIN, GPIO.HIGH)

	def sleep(self,hold=1):
		GPIO.output(self.SLP_PIN, GPIO.LOW)
		time.sleep(hold)
		GPIO.output(self.SLP_PIN, GPIO.HIGH)




