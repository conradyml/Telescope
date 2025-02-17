"""Simple test for using adafruit_motorkit with a stepper motor"""
import time
import board
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

pca = PCA9685(board.I2C(),address=0x60)
pca.frequency = 50
servo1 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2400,actuation_range=135)

for i in range(100):
    kit.stepper1.onestep()
    time.sleep(0.01)

kit.stepper1.release()



servo1.angle=67
time.sleep(1)
servo1.angle=0
time.sleep(1)
servo1.angle=135
time.sleep(1)



for i in range(135):
    servo1.angle = i
    time.sleep(0.03)
for i in range(135):
    servo1.angle = 135 - i
    time.sleep(0.03)

pca.deinit()
