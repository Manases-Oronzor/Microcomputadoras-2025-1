''' This is a micropython program to control the speed
and direction of the motor using seraial communication'''

from machine import Pin, PWM, UART
from L298N_motor import L298N
import time

uart = UART(1, 9600)
uart.init(9600, bits = 8, parity = None,stop = 1, rx = Pin(9), tx = Pin(8))

ENA = PWM(Pin(0))
IN1 = Pin(1, Pin.OUT)
IN2 = Pin(2, Pin.OUT)

motor1 = L298N(ENA, IN1, IN2)
motor1.setSpeed(30000)

while True:
    if uart.any() > 0:
        data = uart.read()
        print(data)
        if "FORWARD" in data:
            motor1.run("FORWARD")
        elif "BACKWARD" in data:
            motor1.run("BACKWARD")
        elif "STOP" in data:
            motor1.run("STOP")
        elif "SPEED" in data:
            uart.write(str(motor1.getSpeed()))
        elif "DIRECTION" in data:
            uart.write(str(motor1.getDirection()))