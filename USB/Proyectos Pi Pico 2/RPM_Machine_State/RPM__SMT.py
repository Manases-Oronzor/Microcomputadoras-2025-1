##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
##  Copyright (c) 2021 by Lucky Resistor. https://luckyresistor.me/  ##
##  See LICENSE file for details.                                    ##
##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##


##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
##  Herramienta para capturar la entrada de RPM de un VENTILADOR  ##
##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##

import rp2
from micropython import const
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio


##############################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####    CODIGO PROPIO AGREGADO PARA PROBAR ESTA RUTINA    ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##############################################################
import machine                              # Importa machine.
machine.freq(125000000)                     # Asegurarse que el procesador
                                            # específicamente va a trabajar
                                            # a 125 Mhz.
                                            # NOTA: Es condición de las
                                            #       máquinas de estado.
from time import sleep, sleep_ms, sleep_us  # Librería de retardos.
import _thread                              # Librería para poder utilizar
                                            # los 2 nucleos.
Pin3 = Pin(3,  Pin.OUT)                     # Pin de acción paralela (que
                                            # generará la onda cuadrada).
                                            # NOTA: vamos a simular que el
                                            #       pin 3 es la entrada de
                                            #       pulsos RPM.
PIN26 = 26                                  # EL pin 26 será la entrada de
                                            # máquina de estado.
                                            
                                            



#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# La frecuencia de la medición #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
FREQ = const(1_000_000)

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# El valor inicial del contador #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
COUNTER_START = const(0x10000)


@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=False, autopush=False)
def measure_rpm():
    ##****************************************************##
    ##  Inicialice X con 0x10000 para valores de 16 bits  ##
    ##****************************************************##
    label("switch_to_low")
    set(x, 1)
    mov(isr, x)
    in_(null, 16)
    mov(x, isr)

    ##*************************************##
    ##  Inicializar el ISR con 0x00000000  ##
    ##*************************************##
    set(y, 0)
    mov(isr, y)

    ##**********************************##
    ##  Esperar nivel sea high estable  ##
    ##**********************************##
    label("wait_for_high")
    in_(pins, 1)
    set(isr, 0)
    mov(y, invert(isr))
    jmp(not_y, "switch_to_high")
    jmp(x_dec, "wait_for_high")

    ##********************************************##
    ##  Nos encontramos con un tiempo de espera,  ##
    ##  enviamos cero, seguimos esperando         ##
    ##********************************************##
    set(y, 0)
    mov(isr, y)
    push(noblock)
    jmp("switch_to_low")

    ##****************************************##
    ##  Inicialice la ISR con el 0xFFFFFFFFF  ##
    ##****************************************##
    label("switch_to_high")
    set(y, 0)
    mov(isr, invert(y))

    ##*************************##
    ##  Espere un low estable  ##
    ##*************************##
    label("wait_for_low")
    in_(pins, 1)
    set(isr, 0)
    mov(y, isr)
    jmp(not_y, "send_data")
    jmp(x_dec, "wait_for_low")


    ##*****************************************************##
    ##  Nos encontramos con un tiempo de espera, enviamos  ##
    ##  cero, reiniciamos.                                 ##
    ##*****************************************************##
    set(y, 0)
    mov(isr, y)
    push(noblock)
    jmp("switch_to_low")

    ##************************************##
    ##  Enviar el contador en este punto  ##
    ##************************************##
    label("send_data")
    mov(isr, x)
    push(noblock)

    ##***********##
    ##  Repetir  ##
    ##***********##
    jmp("switch_to_low")


class RpmInput:

    ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
    ####  Clase para medir una señal de RPM de un ventilador  ####
    ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####

    def __init__(self, sm_id: int, pin: int):
        ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
        ####  Crear una nueva instancia de entrada RPM.        ####
        ####                                                   ####
        ####  :param sm_id: El identificador de la máquina de  ####       
        ####                estado que se utilizará.           ####
        ####  :param pin:   El número de PIN utilizado para    ####
        ####                la entrada.                        ####
        ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####

        self._sm = rp2.StateMachine(sm_id, measure_rpm,freq=FREQ,                         
                                    in_base=Pin(pin,mode=Pin.IN, 
                                    pull=Pin.PULL_UP))
        self._sm.active(1)
        self._value = 0


    def poll(self):
        ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
        ####  Encuesta la interfaz (Poll the interface).    ####
        ####                                                ####
        ####  Llame a este método desde el bucle principal  ####  
        ####  tantas veces como desee.                      ####
        ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
        self._value = self._sm.get()

    def read_rpm(self):
        ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
        ####  Convierta el último valor leído en un valor  ####
        ####  de RPM.                                      ####
        ####                                               ####
        ####  :return: Un valor de RPM, o cero si no se    ####
        ####           recibe señal.                       ####
        ####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
        if self._value == 0:
            return 0
        counts = COUNTER_START - self._value

        ###XOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXO###
        ### signals_per_rotation = 2    (señales_por_rotación)           ###
        ### La fórmula es:                                               ###
        ### 1 / ( counts * 5 * 1/frequency ) / signals_per_rotation * 60 ###                                      
        ###                                                              ###
        ### Resuelve a:                                                  ###
        ### 12 * frequency / counts                                      ###
        ###XOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXO###
#        return 6 * FREQ // counts
        return FREQ






####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        

############################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####                                                    ####
####    PROGRAMA PEINCIPAL PARA PROBAR ESTE PROGRAMA    ####
####                                                    ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
############################################################
        
F_SQUARE = 2               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.


RPM_COUNTER = RpmInput(0,26)


#value = 0
while True:
    print(RPM_COUNTER.read_rpm())
    sleep(1)