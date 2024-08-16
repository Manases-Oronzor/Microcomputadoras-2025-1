
#
# The following assumes Pin 17 is jumper to Pin 16
#
#   from machine import Pin
#
#   pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
#   pin17 = Pin(17, Pin.OUT)
#   pin17.low()
#
#   pc = PulseCounter(0, pin16)
#
#   print("pulse count =", pc.get_pulse_count())
#
#   pin17.high()
#   pin17.low()
#
#   print("pulse count =", pc.get_pulse_count())
#
#   pin17.high()
#   pin17.low()
#
#   print("pulse count =", pc.get_pulse_count())

# https://github.com/dhylands/upy-examples/blob/master/pico/pio_pulse_counter.py 

machine.freq(125000000)  # Example using PIO to count pulses on an input pin.
import rp2

from machine import Pin
import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us                                     
                                     

pin26 = Pin(26, Pin.IN, Pin.PULL_UP)
pin3 = Pin(3, Pin.OUT)



@rp2.asm_pio()
def pulse_counter():
    label("loop")
    # We wait for a rising edge
    wait(0, pin, 0)
    wait(1, pin, 0)
    jmp(x_dec, "loop")  # If x is zero, then we'll wrap back to beginning


class PulseCounter:
    # pin should be a machine.Pin instance
    def __init__(self, sm_id, pin):
        self.sm = rp2.StateMachine(0, pulse_counter, in_base=pin)
        # Initialize x to zero
        self.sm.put(0)
        self.sm.exec("pull()")
        self.sm.exec("mov(x, osr)")
        # Start the StateMachine's running.
        self.sm.active(1)

    def get_pulse_count(self):
        self.sm.exec("mov(isr, x)")
        self.sm.exec("push()")
        # Since the PIO can only decrement, convert it back into +ve
        return -self.sm.get() & 0x7fffffff
    

####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        pin3.off()                # Pon en "0" al Pin GPI
        sleep(HALF)               # Retardo de 0.01 Seg.




F_SQUARE = 1               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
#_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.
                                            
                                            

pc = PulseCounter(0, pin26)
while True:
    pin3.high()
    pin3.low()
#    sleep(0.0001)

    print("pulse count =", pc.get_pulse_count())

