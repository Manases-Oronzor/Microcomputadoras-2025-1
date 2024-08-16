#########################################################
##   RUTINA PARA LEER EL CANAL 0,1 DEL CONVERTIDOR     ##
##   A/D DEL MÓDULO RASPBERRY PI PICO.                 ##
#########################################################
##      UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO        ##
##              FACULTAD DE INGENIERÍA                 ##
##         DEPARTAMENTO DE CONTROL Y ROBÓTICA          ##
#########################################################
##    M. EN I. JOSÉ ANTONIO DE JESÚS ARREDONDO GARZA   ##
##             EMAIL: jarredon@unam.mx                 ##
#########################################################
##                     AÑO 2021                        ##
#########################################################
##
##
##
##    Mp = 70%, F = 1 Hz ===> W = 2*pi+F = 3.1415962 [rad/seg]
##
##    Wo = W/[(1 - Xi^2)^(0.5)]
##
##    Cálculo de Xi en base Mp = Exp(-(piXi)/(1 - Xi^2)^(0.5))
##
##    Wo = (3.1415962)/{[1 - (0.1272170156)^2]^(0.5)]}
##
##    Wo = 3.167331059 [rad/Seg]
##
##    H(s) = (1/LC)/[S^2 + (R/L)S + (1/LC)]
##
##    H(s) = (Wo^2)/[S^2 + 2XiWoS + (Wo^2)]
##
##    H(s) = (10.03198604)/[S^2 + 0.799328083*S + 10.03198604]
##
##    Ts = 0.025 Seg
##
##    H(z) = (0.00155Z^2+0.003099Z+0.00155)/[Z^2-1.974Z+0.9802]
##
##    H(z) = [0.00155+0.003099Z^(-1)+0.00155Z^(-2)]/[1-1.974Z^(-1)+0.9802^(-2)]
##
##    [1-1.974Z^(-1)+0.9802^(-2)]Vo(z) = [0.00155+0.003099Z^(-1)+0.00155Z^(-2)]Vi(z)
##
##    Vo(k) = 0.00155Vi(k) + 0.003099Vi(k-1) + 0.00155Vi(k-2)
##            + 1.974Vo(k-1) - 0.9802Vo(k-2)
##



#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Hacer que la CPU trabaje a 240 Mhz #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
machine.freq(270000000)


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga librería del COnvertidor A/D #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from machine import ADC, Pin
import _thread                       # Librería para poder utilizar
                                     # los 2 nucleos.


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Carga la librería de retardos #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
from time import sleep, sleep_ms, sleep_us


conversion_factor = 1.0 / (65535)   # Factor para que el A/D este entre
                                    # valores 0 y 1
                                    # Mundo discreto -1 <= Z <= +1
adc0 = ADC(Pin(26))                 # Crea el objeto ADC (GPIO26) canal 0.
Pin3 = Pin(3,  Pin.OUT)             # Pin de acción paralela (que generará
                                    # la onda cuadrada).
                                
                                
##################################################
####    ASIGNA COEFICIENTES DE LA ECUACIÓN    ####
####    EN DIFERENCIAS.                       ####
##################################################                                    
A0   = +0.00155
A1   = +0.003099
A2   = +0.00155
B1   = +1.974
B2   = -0.9802
# Condiciones iniciales
UK   = 0.0
UK1  = 0.0
UK2  = 0.0
YK   = 0.0
YK1  = 0.0
YK2  = 0.0


####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####   HILO GENERADOR DE ONDA CUADRADA CON 2DO NÚCLEO   ####
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
def Onda_Cuadrada():
    while True:
        Pin3.on()                 # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.
        Pin3.off()                # Pon en "0" al Pin GPIO3 de la RP2.
        sleep(HALF)               # Retardo de 0.01 Seg.



##############################################################
####    PROGRAMA PARA HACER EL FILTRADO EN TIEMPO REAL    ####
##############################################################

F_SQUARE = 0.0625               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.


while True:
    YK = A0*UK + A1*UK1 + A2*UK2 + B1*YK1 + B2*YK2

    # Actualiza I/O para la próxima iteración
    UK2 = UK1
    UK1 = UK
    YK2 = YK1
    YK1 = YK
    Read0 = adc0.read_u16() * conversion_factor  # Toma lectura del canal 0
                                                 # del ADC en volts reales.
    UK = Read0                                   # Asigna el nuevo valor U(k).
    print((UK,YK))                               # Grafica y muestra datos.
    sleep(0.025)                                 # Retardo de 0.025 Seg que
                                                 # corresponde al tiempo
                                                 # de muestreo.
