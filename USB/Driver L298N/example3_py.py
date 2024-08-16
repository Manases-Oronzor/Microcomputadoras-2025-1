"""This micropython program makes the motor1 
move in forward and backward directions with
increasing speed."""

from machine import Pin, PWM
from L298N_motor import L298N
import time

ENA = PWM(Pin(0))        
IN1 = Pin(1, Pin.OUT)         
IN2 = Pin(2, Pin.OUT)

motor1 = L298N(ENA, IN1, IN2)     #create a motor1 object
motor1.setSpeed(25000)            #set the speed of motor1. Speed value varies from 25000 to 65534

while True:
    for speed in range(25000, 65000, 100):
        motor1.setSpeed(speed)
        motor1.forward()
        time.sleep(0.1)
    motor1.stop()
    for speed in range(25000, 65000, 100):
        motor1.setSpeed(speed)
        motor1.backward()
        time.sleep(0.1)
    motor1.stop()