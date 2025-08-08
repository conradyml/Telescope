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
		print("Enter move")
		if steps<0:
			print("Steps are negative")
			steps=abs(steps)
			if direction == REVERSE:
				direction = FORWARD
			else:
				direction = REVERSE
		print("Calling move threaded")
		if self.thread is not None and self.thread.is_alive():
			print("Thread is running")
			self.interrupt.set()
			print("Thread Interrupted.")
			self.thread.join()
			self.interrupt.clear()
			print ("Interrupt Cleared.")
		self.thread = threading.Thread(target=self.move_threaded, args=(steps,direction,speed,callback, callback_interval))
		self.thread.start()
		print("Exit move")

		#return count

	def move_threaded(self, steps, direction, speed, callback, callback_interval):
		print("Enter move_threaded")
		count=0
		
	#	print("move_threaded: before while")
		while not self.interrupt.is_set() and count < steps:
	#		print("Enter While 1")
			GPIO.output(self.DIR_PIN, direction)
			delay = 1 / speed
			#for _ in range(steps):
			GPIO.output(self.STEP_PIN, GPIO.HIGH)
			time.sleep(delay)
			GPIO.output(self.STEP_PIN, GPIO.LOW)
			time.sleep(delay)
			count+=1
			if (count % callback_interval) ==0:
				if direction == REVERSE:
					callback(-callback_interval)
				else:
					callback(callback_interval)
	#	print("move_threaded: end while")
		if direction == REVERSE:
			callback(-count % callback_interval)
		else:
			callback(count % callback_interval)
		print("Exit move_threaded")

	def stop(self):
		if self.thread is not None and self.thread.is_alive():
			print("Thread is running")
			self.interrupt.set()
			print("Thread Interrupted.")
			self.thread.join()
			self.interrupt.clear()

	def reset(self,hold=1):
		GPIO.output(self.SLP_PIN, GPIO.HIGH)
		GPIO.output(self.RST_PIN, GPIO.LOW)
		time.sleep(hold)
		GPIO.output(self.RST_PIN, GPIO.HIGH)

	def sleep(self):
		GPIO.output(self.SLP_PIN, GPIO.LOW)
		
	def wake(self):	
		GPIO.output(self.SLP_PIN, GPIO.HIGH)




