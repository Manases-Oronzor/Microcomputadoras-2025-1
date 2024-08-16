
# https://forum.micropython.org/viewtopic.php?t=11463

from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio
import time
machine.freq(125000000)



import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.
from time import sleep, sleep_ms, sleep_us


                          
F_SQUARE = 1000               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.           

Pin3 = Pin(3,  Pin.OUT)    # Pin de acción paralela (que generará
                           # la onda cuadrada).



## ESTA RUTINA DEVUELVE LA DURACIÓN ENTRE PULSOS ##
@rp2.asm_pio(set_init=rp2.PIO.IN_LOW, autopush=True, push_thresh=32)
def period():
    wrap_target()
    set(x, 0)
    wait(0, pin, 0)              # Wait for pin to go low
    wait(1, pin, 0)              # Low to high transition
    label('low_high')
    jmp(x_dec, 'next') [1]       # unconditional
    label('next')
    jmp(pin, 'low_high')         # while pin is high
    label('low')                 # pin is low
    jmp(x_dec, 'nxt')
    label('nxt')
    jmp(pin, 'done')             # pin has gone high: all done
    jmp('low')
    label('done')
    in_(x, 32)                   # Auto push: SM stalls if FIFO full
    wrap()



## ESTA RUTINA DEVUELVE LA DURACIÓN DEL PULSO ##
@rp2.asm_pio(set_init=rp2.PIO.IN_LOW, autopush=True, push_thresh=32)
def mark():
    wrap_target()
    set(x, 0)
    wait(0, pin, 0)  # Wait for pin to go low
    wait(1, pin, 0)  # Low to high transition
    label('low_high')
    jmp(x_dec, 'next') [1]  # unconditional
    label('next')
    jmp(pin, 'low_high')  # while pin is high
    in_(x, 32)  # Auto push: SM stalls if FIFO full
    wrap()




#pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
pin16 = Pin(26, Pin.IN, Pin.PULL_UP)    
sm0   = rp2.StateMachine(0, period, in_base=pin16, jmp_pin=pin16)
sm0.active(1)

sm1   = rp2.StateMachine(1, mark, in_base=pin16, jmp_pin=pin16)
sm1.active(1)




#pwm = PWM(Pin(17))  # OJO OJO OJO
#pwm = PWM(Pin(3))
#pwm.freq(8000)
#pwm.duty_u16(0xffff // 3)



####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        time.sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        time.sleep(HALF)               # Retardo de 0.01 Seg.






_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.

# Clock is 125MHz. 3 cycles per iteration, so unit is 24.0ns
def scale(v):
    return (1 + (v ^ 0xffffffff)) * 24e-6  # Scale to ms

while True:
    period = scale(sm0.get())
    mark = scale(sm1.get())
    print(period, mark, mark/period)
    F = (1/period)*1000
    print("FRECUENCIA = " + str(F))
    time.sleep(1)