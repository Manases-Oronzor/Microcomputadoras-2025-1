

from machine import Pin, Timer
import time

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us

import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.
Pin3 = Pin(3,  Pin.OUT)    # Pin de acción paralela (que generará
                           # la onda cuadrada).
Pin25 = Pin(25,  Pin.OUT) 


period  = 5000  #5000
counter = 0
U_min   = 0

hall = Pin(26, Pin.IN, Pin.PULL_UP)


## IRQ Trigger
def hall_trigger(input):
    global counter
    counter += 1
#    print(input)
    
def freq_update(input):
    global counter, U_min
    U_min = int(counter/(period/1000)*60)
    counter = 0
    print(U_min)
    print('OK')
    print('Revoluciones')
    print('    ')


    
# IRQ_HALL
hall.irq(trigger = Pin.IRQ_FALLING, handler = hall_trigger)

# TIMER
timer = Timer()
timer.init(period = period, mode = Timer.PERIODIC, callback = freq_update)



####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        Pin25.on()
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        Pin25.off()
        sleep(HALF)               # Retardo de 0.01 Seg.
        
        
        
F_SQUARE = 50               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.
                                            
while True:
    sleep(1)