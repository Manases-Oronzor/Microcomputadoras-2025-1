#########################################################
##   RUTINA PARA LEER EL CANAL 0 DEL CONVERTIDOR       ##
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
##    H(s) = [2/(S+2)] para Tau = 0.5 Seg
##
##    Ts = 0.025 Seg
##
##    Tustin:  S = (2/T)([Z-1]/[Z+1])
##
##    MATLAB:
##    >> Sys = tf([0 2],[1 2])
##    >> step(Sys)        % Gráfica de respuesta
##    >> bode(Sys)        % Resp en frecuencia
##    >> Sysd = c2d(Sys,0.025,'Tustin')
##    >> step(Sysd)
##
##    H(z) = (0.02439Z + 0.02439)/(Z - 0.9512)
##
##    Desnormalización (entre Z de mayor orden del denominador):
##
##    H(z) = (0.02439 + 0.02439Z^(-1))/(1 - 0.9512Z^(-1))
##
##    Vo(z)[1 - 0.9512Z^(-1)] = Vi(z)[0.02439 + 0.02439^(-1)]
##
##    f(z) ==> f(k)  evento actual
##    f(z)*Z^(-n) ==> f(k-n)  Eventos pasados
##    f(z)*Z^(-n) ==> f(k+n)  Eventos futuros
##
##    Vo(k) - 0.9512Vo(k-1) = 0.02439Vi(k) + 0.02439Vi(k-1)
##
##    Vo(k) = 0.02439Vi(k) + 0.02439Vi(k-1) + 0.9512Vo(k-1)
##
##    Suma de Prductos "MAC":
##
##    Filtro de respuesta a impulso infinita IIR:
##    Y(k) = SUMATORIA{a(i)*U(k-i)} + SUMATORIA{bm*Y(k-m)}
##           0 - I                    1 - M
##
##    Physnionet



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
CTE_A0 = 0.02439
CTE_A1 = 0.02439
CTE_B1 = 0.9512
# Condiciones iniciales
UK     = 0.0           # u(k1)
UK1    = 0.0           # u(k-1)
YK     = 0.0           # y(k)
YK1    = 0.0           # y(k-1)




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

F_SQUARE = 0.25               # Frecuencia de la onda cuadrada = 1 Hz.
PERIODO  = (1/F_SQUARE)    # Obten el periodo de la senal
                           # (inverso de la frecuencia).
HALF     = (PERIODO/2)     # Obten el semiperiodo de la señal
                           # para la rutina generadora de
                           # onda cuadrada con el nucleo 2.
_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de
                                            # la onda cuadrada.

while True:
    YK = CTE_A0*UK + CTE_A1*UK1 + CTE_B1*YK1

    # Actualiza I/O para la próxima iteración
    UK1 = UK
    YK1 = YK
    Read0 = adc0.read_u16() * conversion_factor  # Toma lectura del canal 0
                                                 # del ADC en volts reales.
    UK = Read0                                   # Asigna el nuevo valor U(k).
    print((UK,YK))                               # Grafica y muestra datos.
    sleep(0.025)                                 # Retardo de 0.025 Seg que
                                                 # corresponde al tiempo
                                                 # de muestreo.
