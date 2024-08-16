#  Copyright (c) 2021 by Lucky Resistor. https://luckyresistor.me/
#  See LICENSE file for details.
"""
Tool to capture RPM input from a FAN.
"""
import rp2
from micropython import const
from machine import Pin

machine.freq(125000000)

import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us

Pin3 = Pin(3,  Pin.OUT)    # Pin de acción paralela (que generará
                           # la onda cuadrada).





# The frequency for the measurement.
FREQ = const(1_000_000)
# The counter start value.
COUNTER_START = const(0x10000)


@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=False, autopush=False)
def measure_rpm():
    # Initialize X with 0x10000 for 16bit values
    label("switch_to_low")
    set(x, 1)
    mov(isr, x)
    in_(null, 16)
    mov(x, isr)
    # Initialize the ISR with 0x00000000
    set(y, 0)
    mov(isr, y)
    # wait for stable high
    label("wait_for_high")
    in_(pins, 1)
    set(isr, 0)
    mov(y, invert(isr))
    jmp(not_y, "switch_to_high")
    jmp(x_dec, "wait_for_high")
    # We run into a timeout, send zero, keep waiting
    set(y, 0)
    mov(isr, y)
    push(noblock)
    jmp("switch_to_low")
    # Initialize the ISR with the 0xFFFFFFFFF
    label("switch_to_high")
    set(y, 0)
    mov(isr, invert(y))
    # Wait for a stable low
    label("wait_for_low")
    in_(pins, 1)
    set(isr, 0)
    mov(y, isr)
    jmp(not_y, "send_data")
    jmp(x_dec, "wait_for_low")
    # We ran into a timeout, send zero, restart.
    set(y, 0)
    mov(isr, y)
    push(noblock)
    jmp("switch_to_low")
    # Send the counter at this point
    label("send_data")
    mov(isr, x)
    push(noblock)
    # Repeat
    jmp("switch_to_low")
    
    
class RpmInput:
    """
    Class to measure a RPM signal from a fan.
    """
    def __init__(self, sm_id: int, pin: int):
        """
        Create a new RPM input instance.
        :param sm_id: The state machine identifier to use.
        :param pin: The pin number used for the input.
        """
        self._sm = rp2.StateMachine(sm_id, measure_rpm,
                                    freq=FREQ,
                                    in_base=Pin(pin, mode=Pin.IN, pull=Pin.PULL_UP))
        self._sm.active(1)
        self._value = 0
    def poll(self):
        """
        Poll the interface.
        Call this method from the main loop as often as you like.
        """
        self._value = self._sm.get()
    def read_rpm(self):
        """
        Convert the last read value into an RPM value.
        :return: A RPM value, or zero if no signal received.
        """
        if self._value == 0:
            return 0
        counts = COUNTER_START - self._value
        # signals_per_rotation = 2
        # Formula is: 1 / ( counts * 5 * 1/frequency ) / signals_per_rotation * 60
        # Solves to: 12 * frequency / counts
        return 6 * FREQ // counts
    
    
    
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.   




F_SQUARE = 5               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
#_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.




Medidor = RpmInput(1,26)
while True:
    Pin3.on()
    Pin3.off()
    print(Medidor.read_rpm())
    sleep(1)