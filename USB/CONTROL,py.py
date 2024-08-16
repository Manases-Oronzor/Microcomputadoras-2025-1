

from machine import Pin, PWM

P0 = Pin(0, Pin.OUT)
P1 = Pin(1, Pin.OUT)

from time import sleep, sleep_ms, sleep_us

PWM0 = PWM(Pin(1))
PWM0.freq(70)


while True:
    Modulation = 20000
    PWM0.duty_u16(Modulation)
    print("En Movimiento")
    sleep(2)
    Modulation = 0
    PWM0.duty_u16(Modulation)
    print("Motor Parado")
    sleep(2)
    