# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""

import time
import board
import busio
import pwmio

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from adafruit_motor import servo


servopin = MotorKit._pca.channels[1]
kit=MotorKit(address=0x60)


servo14=servo.Servo(servopin, min_pulse=500, max_pulse=2400)
servo14.actuation_range=135

# We sleep in the loops to give the servo time to move into position.
for i in range(120):
    servo14.angle = i
    time.sleep(0.03)
for i in range(120):
    servo14.angle = 120 - i
    time.sleep(0.03)

kit = MotorKit(address=0x60)

for i in range(200):
    kit.stepper1.onestep()
    time.sleep(0.01)

kit.stepper1.release()

for i in range(200):
    kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
    time.sleep(0.01)

kit.stepper2.release()



