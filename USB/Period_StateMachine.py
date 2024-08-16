
# https://forum.micropython.org/viewtopic.php?t=11463

from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio
import time
machine.freq(125000000)


ENABLE = Pin(0)
Pin2   = Pin(2)



## ESTA RUTINA DEVUELVE LA DURACIÓN ENTRE PULSOS ##
@rp2.asm_pio(set_init=rp2.PIO.IN_LOW, autopush=True, push_thresh=32)
def period():
    wrap_target()
    set(x, 0)
    wait(0, pin, 0)              # Espere a que el pin baje
    wait(1, pin, 0)              # Transición de bajo a alto
    label('low_high')
    jmp(x_dec, 'next') [1]       # Incondicional
    label('next')
    jmp(pin, 'low_high')         # Mientras el pin está alto
    label('low')                 # El pin está bajo
    jmp(x_dec, 'nxt')
    label('nxt')
    jmp(pin, 'done')             # El pin ha subido: todo hecho
    jmp('low')
    label('done')
    in_(x, 32)                   # Auto push: SM se detiene si FIFO está lleno
    wrap()



## ESTA RUTINA DEVUELVE LA DURACIÓN DEL PULSO ##
@rp2.asm_pio(set_init=rp2.PIO.IN_LOW, autopush=True, push_thresh=32)
def mark():
    wrap_target()
    set(x, 0)
    wait(0, pin, 0)              # Espere a que el pin baje
    wait(1, pin, 0)              # Transición de bajo a alto
    label('low_high')
    jmp(x_dec, 'next') [1]       # Incondicional
    label('next')
    jmp(pin, 'low_high')         # Mientras el pin está alto
    in_(x, 32)                   # Auto push: SM se detiene si FIFO está lleno
    wrap()




#pin16 = Pin(16, Pin.IN, Pin.PULL_UP)
pin16 = Pin(26, Pin.IN, Pin.PULL_UP)    
sm0   = rp2.StateMachine(0, period, in_base=pin16, jmp_pin=pin16)
sm0.active(1)

sm1   = rp2.StateMachine(1, mark, in_base=pin16, jmp_pin=pin16)
sm1.active(1)




ENABLE.on()
Pin2.on()

#pwm = PWM(Pin(17))
pwm = PWM(Pin(1))
pwm.freq(200)
pwm.duty_u16(0xffff // 3)
#time.sleep(5)
#ENABLE.off()



# Clock is 125MHz. 3 cycles per iteration, so unit is 24.0ns
def scale(v):
    return (1 + (v ^ 0xffffffff)) * 24e-6  # Escalar a milisegundos





while True: 
    period = scale(sm0.get())            # Obten el periodo.
    mark = scale(sm1.get())              # Calcula duración del pulso
#    print(period, mark, mark/period)     #
    print("PERIODO = " + str(period) + " mSeg")
    print("MARK = " + str(mark))
    print("PROMEDIO = " + str(mark/period))
    F = (1/period)*1000
    print("FRECUENCIA = " + str(F) +  " Hertz")
    RPM = (F*60)/374.22
    print("RPM = " + str(RPM))
    time.sleep(1)