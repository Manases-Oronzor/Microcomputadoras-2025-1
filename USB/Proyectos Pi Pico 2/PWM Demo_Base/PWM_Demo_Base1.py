#############################################################
#############################################################
####                                                     ####
####   EJEMPLO QUE REALIZA UN CAMBIO DE INTENSIDAD DEL   ####
####   PIN 25.                                           ####
####                                                     ####
#############################################################
#############################################################
####                                                     ####
####       UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO       ####
####               FACULTAD DE INGENIERÍA                ####
####                                                     ####
#############################################################
#############################################################
####                                                     ####
####    M. EN I. JOSÉ ANTONIO DE JESÚS ARREDONDO GARZA   ####
####              EMAIL: jarredon@unam.mx                ####
####                      MARZO 2024                     ####
####                                                     ####
#############################################################
#############################################################

import machine              # Importa machine.
machine.freq(270000000)     # Cambia reloj a 270 Mhz.


#####################################
#  Trae la Librería de Pines y PWM  #
#####################################
from machine import Pin, PWM

##################################
#  Trae la Librería de Retardos  #
##################################

from time import sleep, sleep_ms, sleep_us

##########################################################
####  Hay 8 canales independientes, cada uno de los   ####
####  cuales tiene 2 salidas, lo que hace 16 canales  ####
####  PWM en total que se pueden sincronizar desde    ####
####  7Hz a 125Mhz.                                   ####
##########################################################

PWM0 = PWM(Pin(25))        # Crea el objeto PWM en Pin 25.
PWM0.freq(50000)           # La freciencia es de 50,000 Hz.

####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####  PROGRAMA PRINCIPAL PARA MODULAR LA INTENSIDAD  ####
####  DEL PIN 25 (NATIVO).                           ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####

while True:
    Modulation = 0                     # Inicia Modulación en cero.
    
    #********************#
    # Loop de control de #
    # intensidad.        #
    #********************#
    for i in range(0, 255):
        PWM0.duty_u16(Modulation)      # Rango de PWM de 0 - 65535.
        sleep_ms(5)                    # Retardo de 5 milisegundos.
        Modulation = Modulation + 256  # Incrementos de 256
        
    #********************************#
    # Pon en cero a la PWM (apagado) #
    #********************************#
    PWM0.duty_u16(0)                    # Modulación en creo.
    sleep(1)                            # Retardo de 1 Segundo.

####################################
#  Deshabilita el Pin25 de la PWM  #
####################################
PWM0.deinit()                           # Apagua PWM en el Pin 25.