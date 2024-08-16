''' This is a micropython program to control the
speed of motor1 using a potentiometer'''

from machine import Pin, PWM, ADC
from L298N_motor import L298N
import time

potentiometer = ADC(26)
ENA = PWM(Pin(0))        
IN1 = Pin(1, Pin.OUT)         
IN2 = Pin(2, Pin.OUT)

motor1 = L298N(ENA, IN1, IN2)

while True:
    reading = potentiometer.read_u16()
    motor1.setSpeed(int(reading))
    motor1.forward()
    time.sleep(0.1)