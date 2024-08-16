
# https://forums.raspberrypi.com/viewtopic.php?t=307715    


# Tienes que encontrar un buen microprocesador para conseguir hasta 8
# contadores que puedan funcionar hasta 30Mhz sin problema.

# Mi clase de contador


from machine import Pin,Timer, PWM
from rp2 import PIO, asm_pio, StateMachine

machine.freq(125000000)

import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us

Pin3 = Pin(3,  Pin.OUT)    # Pin de acción paralela (que generará
                           # la onda cuadrada).
 
 
 
@asm_pio()    
def PIO_COUNTER():
    set(x,0)
    wrap_target()
    label('loop')
    wait(0,pin,0)
    wait(1,pin,0)
    jmp(x_dec,'loop')
    wrap()
 
 
 
class SMCounter:
    
    def __init__(self, smID, InputPin):
        self.counter = 0x0
        self.sm = StateMachine(smID)
        self.pin = InputPin
        self.sm.init(PIO_COUNTER,freq=125_000_000,in_base=self.pin)
        self.sm.active(1)
    
    def value(self):
        self.sm.exec('mov(isr,x)')
        self.sm.exec('push()')
        self.counter = self.sm.get()
        return  (0x100000000 - self.counter) & 0xffffffff
    
    def reset(self):
        self.sm.active(0)
        self.sm.init(PIO_COUNTER,freq=125_000_000,in_base=self.pin)
        self.sm.active(1)
        

    def __del__(self):
        self.sm.active(0)


# Un código simple que se parece a lo que quieres.



#from SMCounter import SMCounter
#from machine import Pin
#import utime


counter = SMCounter(smID=0,InputPin=Pin(26,Pin.IN,Pin.PULL_UP))



####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.





F_SQUARE = 300               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.




Last_Value = 0
while True:
    Present_Value = counter.value()
    VALOR = Present_Value - Last_Value
    Last_Value = Present_Value
    print(VALOR)
    sleep(1)