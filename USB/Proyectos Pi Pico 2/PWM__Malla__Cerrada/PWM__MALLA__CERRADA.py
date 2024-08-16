################################################################
################################################################
####                                                        ####
####   CONTROL EN MALLA CERRADA DE UN MOTOR DE CORRIENTE    ####
####   DIRECTA USANDO COMO ENTRADA AL CANAL ANO DEL A/D,    ####
####   UNA PWM EN COMBINACIÓN CON UN MOSFET IRLZ44, UN      ####
####   DISCO ÓPTICO CON 6 MUESCAS EN COMBINACIÓN Y UNA      ####
####   RASPBERRY PI PICO.                                   ####
####                                                        ####
####   NOTA: LA ALIMENTACIÓN DEL TRANSISTOR ES A +5V DE     ####
####         LA SIGUIENTE MANERA                            ####
####                                                        ####
####        +5V__________________                           ####
####                             |                          ####
####                             |                          ####
####                           MOTOR --> ENCODER OPTICO     ####
####                             |                          ####
####                             |                          ####
####                          (drain)                       ####
####                             |                          ####
####        PWM --> (gate) --> MOSFET                       ####
####                             |                          ####
####                          (source)                      ####
####                             |                          ####
####                             |                          ####
####                            GND                         ####
####                                                        ####
####    NOTA: PARA MEDIR LA FRECUENCIA DE RETROALIMENTA-    ####
####          CIÓN SE EMPLEARÁN MÁQUINAS DE ESTADO.         ####
####                                                        ####
################################################################
################################################################
####                                                        ####
####        UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO         ####
####                FACULTAD DE INGENIERÍA                  ####
####                                                        ####
################################################################
################################################################
####                                                        ####
####     M. EN I. JOSÉ ANTONIO DE JESÚS ARREDONDO GARZA     ####
####                 EMAIL: jarredon@unam.mx                ####
####                       MARZO 2024                       ####
####                                                        ####
################################################################
################################################################


import machine                      # Importar la librería machine.
machine.freq(270000000)             # Asegurarse que el procesador 
                                    # trabaje a 270 Mhz. 


#################################################
#  Trae la Librería de Pines, PWM, ADC e HILOS  #
#################################################
from machine import Pin, PWM, ADC
import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.


##################################
#  Trae la Librería de Retardos  #
##################################
from time import sleep, sleep_ms, sleep_us


####################################################
##  CONFIGURACIÓN DEL PIN26 COMO ENTRADA AN0 DEL  ##
##  CONVERTIDOR A/D. ESTO ES:                     ##               
##  READ = (ANALOG << 4) ==> Emula (2^16 - 1)     ##
####################################################
ADC0  = ADC(Pin(26))        # Crea el objeto ADC (GPIO26) canal 0
PWM0  = PWM(Pin(15))        # Crea el objeto PWM en Pin 15 y este
                            # va a ser la salida de la PWM.
                            # NOTA: a la mejor se requiere declarar
                            #       el Pin 15 como salida.
PWM0.freq(1000)             # La freciencia es de 1000 Hz.
READY = 0                   # Bandera indicadora de cuenta lista
                            # (del sensor óptico).
CUENTA = 0


##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
##  El pin 16 va a ser el que recibe los pulsos  ##
##  del ENCODER OPTICO.                          ##
##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
PIN16 = Pin(16, Pin.IN, Pin.PULL_UP)


def PULSOS():
    if PIN16 == 0:
        CUENTA = CUENTA + 1









while True:
    READ = ADC0.read_u16() # Lee el valor absoluto del A/D
                           # (o sea, un valor entre 0 y
                           #  655535).