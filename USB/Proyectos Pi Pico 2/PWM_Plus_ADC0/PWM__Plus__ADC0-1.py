##################################################################
##################################################################
####                                                          ####
####    RUTINA PARA LEER EL CANAL AN0 DEL CONVERTIDOR A/D,    ####
####    EMPLEAR EL VALOR LEÍDO PARA MODULAR A UNA PWM.        ####
####                                                          ####
####    LA ENTRADA DEL CONVERTIDOR A/D PROVENDRÁ DE UNA       ####
####    SEÑAL CUADRADA GENERADA POR EL NUCLEO 2 DE LA RP2.    ####
####                                                          ####
####    LA FRECUENCIA DE MUESTREO Fs QUE SE ELIGIÓ EN EL      ####
####    LOOP DEL PRIMER NUCLEO ES DE 1000 HZ.                 ####
####                                                          ####
##################################################################
##################################################################
####                                                          ####
####         UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO          ####
####                 FACULTAD DE INGENIERÍA                   ####
####                                                          ####
##################################################################
##################################################################
####                                                          ####
####      M. EN I. JOSÉ ANTONIO DE JESÚS ARREDONDO GARZA      ####
####                  EMAIL: jarredon@unam.mx                 ####
####                        MARZO 2024                        ####
####                                                          ####
##################################################################
##################################################################

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Hacer que la CPU trabaje a 240 Mhz #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
machine.freq(270000000)


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga librería del COnvertidor A/D #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from machine import ADC, Pin, PWM
import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us




####################################################
##  CONFIGURACIÓN DEL PIN26 COMO ENTRADA AN0 DEL  ##
##  CONVERTIDOR A/D. ESTO ES:                     ##               
##  READ = (ANALOG << 4) ==> Emula (2^16 - 1)     ##
####################################################
ADC0 = ADC(Pin(26))        # Crea el objeto ADC (GPIO26) canal 0
Pin3 = Pin(3,  Pin.OUT)    # Pin de acción paralela (que generará
                           # la onda cuadrada).



##########################################################
####  Hay 8 canales independientes, cada uno de los   ####
####  cuales tiene 2 salidas, lo que hace 16 canales  ####
####  PWM en total que se pueden sincronizar desde    ####
####  7Hz a 125Mhz.                                   ####
##########################################################
PWM0 = PWM(Pin(25))        # Crea el objeto PWM en Pin 25.
PWM0.freq(50000)           # La freciencia es de 50000 Hz.


####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.




####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   RUTINA PRINCIPAL QUE EJEMPLIFICA UNA MODULACIÓN   ####
####   SIMPLE UTILIZANDO EN VALOR ABSOLUTO QUE SE LEE    ####
####   DEL CANAL AN0 DEL CONVERTIDOR A/D COMO VALOR DE   ####
####   MODULACIÓN.                                       ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##############################################################
####    PROGRAMA PARA HACER EL FILTRADO EN TIEMPO REAL    ####
##############################################################

F_SQUARE = 1               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.
                           
while True:
    READ = ADC0.read_u16() # Lee el valor absoluto del A/D
                           # (o sea, un valor entre 0 y
                           #  655535).
    PWM0.duty_u16(READ)    # La salida del A/D va a modular
                           # al canal PWM.
    sleep_ms(1)            # Realiza un retardo de 1 mSeg que
                           # equivale a una frecuencia de
                           # muestreo Fs = 1000 Hz.

    

####################################
#  Deshabilita el Pin25 de la PWM  #
####################################
PWM0.deinit()                           # Apagua PWM en el Pin 25.