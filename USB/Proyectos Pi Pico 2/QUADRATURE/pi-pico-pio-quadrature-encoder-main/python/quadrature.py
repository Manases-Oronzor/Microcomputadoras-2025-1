# SPDX-FileCopyrightText: 2022 Jamon Terrell <github@jamonterrell.com>
# SPDX-License-Identifier: MIT

from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
import utime

machine.freq(125000000)

import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.
                                     
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us

Pin3 = Pin(3,  Pin.OUT)    # Pin de acción paralela (que generará
                           # la onda cuadrada).                                     
Pin2 = Pin(2,  Pin.OUT)


@asm_pio(autopush=True, push_thresh=32)
def encoder():
    label("start")
    wait(0, pin, 0)         # Wait for CLK to go low
    jmp(pin, "WAIT_HIGH")   # if Data is low
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop1")
    label("nop1")
    mov(x, invert(x))
    label("WAIT_HIGH")      # else
    jmp(x_dec, "nop2")          # Decrement X
    label("nop2")
    
    wait(1, pin, 0)         # Wait for CLK to go high
    jmp(pin, "WAIT_LOW")    # if Data is low
    jmp(x_dec, "nop3")          # Decrement X
    label("nop3")
    
    label("WAIT_LOW")       # else
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop4")
    label("nop4")
    mov(x, invert(x))
    wrap()



####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
#        Pin2.off()
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
#        Pin2.on()
        sleep(HALF)               # Retardo de 0.01 Seg.



F_SQUARE = 5               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.




    
#sm1 = StateMachine(1, encoder, freq=125_000_000, in_base=Pin(3), jmp_pin=Pin(2))
sm1 = StateMachine(1, encoder, freq = 125_000_000, in_base = Pin(26), jmp_pin = Pin(26))
sm1.active(1)


while(True):
    Pin2.on()
    Pin2.off()
    utime.sleep(1)
    sm1.exec("in_(x, 32)")
    x = sm1.get()
    print(x)
#    Pin2.on()
#    Pin2.off()
