#######################################################################
#######################################################################
####                                                               ####
####          UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO              ####
####                  FACULTAD DE INGENIERÍA                       ####
####            DEPARTAMENTO DE CONTROL Y ROBÓTICA                 ####
####                                                               ####
#######################################################################
#######################################################################
####                                                               ####
####                       NOTA IMPORTANTE 1                       ####
####  ESTE PROGRAMA IMPLEMENTA UNA ECUACIÓN EN DIFERENCIAS DE 2DO  ####
####  ORDEN GENÉRICA A UNA TASA DE MUESTREO APROXIMADA DE 8 KHZ Y  ####
####  ES CAPAZ DE ACTUALIZAR LOS COEFICIENTES PROVENIENTES DE LA   ####
####  INTERFAZ DE MATLAB.                                          ####
####                                                               ####
####                       NOTA IMPORTANTE 2                       ####
####  SI SE DESEA IMPLEMENTAR UNA ECUACIÓN EN DIFERENCIAS DE 1ER   ####
####  ORDEN SOLO BASTA PONER EN CEROS A LOS COEFICIENTES A2 Y B2.  ####
####                                                               ####
####                       NOTA IMPORTANTE 3                       ####
####  LA FRECUENCIA DE ENTRADA ASIGNADA A LA ECUACIÓN SE PUEDE     ####
####  VARIAR TAMBIEN VÍA MATLAB Y ESTA ES GOBERNADA POR EL 2DO     ####
####  NUCLEO DE LA RP2040 UTILIZANDO UN "THREAD". SE ASUME QUE     ####
####  LA SEÑAL GENERADA ES UNA ONDA CUADRADA CON UNA AMPLITUD DE   ####
####  +3.3 VOLTS.                                                  ####
####                                                               ####
####                       NOTA IMPORTANTE 4                       ####
####  LA APPDESIGNER DE MATLAB ENVÍA INICIALMENTE UNOS COEFICIEN-  ####
####  DE PRUEBA PARA UNA FUNCIÓN DE 1ER ORDEN.                     ####
####  MATLAB REALIZA UN CICLO DE SIMULACIÓN DE 30 SEGUNDOS.        ####
####                                                               ####
####                       NOTA IMPORTANTE 5                       ####
####  PARA EVITAR PROBLEMAS CON LA INTERFAZ DE MATLAB SE RECOMIEN- ####
####  GUARDAR EL ARCHIVO EN LA MEMORIA FLASH DE LA RP2040 CON EL   ####
####  NOMBRE "main.py" Y ASÍ ESTE SE EJECUTARA AL ENCENDER LA      ####
####  RP2040.                                                      ####
####                                                               ####
#######################################################################
#######################################################################
####                                                               ####
####       M. EN I. JOSÉ ANTONIO DE JESÚS ARREDONDO GARZA          ####
####                 EMAIL: jarredon@unam.mx                       ####
####                          MAYO 2023                            ####
####                                                               ####
#######################################################################
#######################################################################


from machine import Pin, Timer               # Importa librería de Pines.
from time import sleep, sleep_ms, sleep_us   # Importa librerías de retardos.
from machine import ADC,UART                 # Importa librerías del A/D y la UART.
import       _thread                         # Librería para poder utilizar
                                             # los 2 nucleos.


#OXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOX#
# Convertir float a Hexadecimal  #
#OXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOX#

import struct


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#
# Hacer que la CPU trabaje a 240 Mhz #
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX#

machine.freq(270000000)


####################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####################################################################                                        
####                                                            ####                                        
####        CONFIGURA EL CANAL ADC0 DEL CONVERTIDOR A/D.        ####
####                                                            ####
####################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
####################################################################

ADC0 = ADC(Pin(26))                 # Define el objeto ADC (GPI26)
                                    # canal 0.
P25  = Pin(25, Pin.OUT)             # Pin nativo de la tarjeta
                                    # como testigo.
Pin3  = Pin(3,  Pin.OUT)            # Pin de acción paralela (que generará
                                    # la onda cuadrada).


#######################################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#######################################################################################
####                                                                               ####                           
####    CONFIGURA LA UART0 @ 460800 BAUDS, 8 BITS, 1 START, 1 STOP, ASOCIADOS A    ####
####    LOS PINES: GPIO0 = Tx y GPIO1 = Rx                                         ####
####                                                                               ####
#######################################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
#######################################################################################
                           
UART0 = UART(0, baudrate = 460800, tx = Pin(0), rx = Pin(1))   # Para un HC05 460800 bauds


############################################################################
####OXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOx####
############################################################################
####                                                                    ####
####          VARIABLES DEL PROGRAMA PRINCIPAL EN MICROPYTHON           ####
####                                                                    ####
############################################################################
####OXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOXOx####
############################################################################


COUNTER = 0                         # Contador de muestras.
conversion_factor = 3.3 / (65535)   # Factor de conversión para
                                    # que el A/D esté entre
                                    # valores de 0 a 3.3 Volts.
MUESTRAS = 1000                     # Número de muestras.
ENTRADAS = [0]*MUESTRAS             # Variable que contendrá la
                                    # lectura del A/D (CANAL 0).
                                    # NOTA: esta variable contendrá
                                    #       el npumero de muestras
                                    #       (que en este caso serán
                                    #        500).
SALIDAS  = [0]*MUESTRAS             # Variable que contendrá las
                                    # salidas de Vo(k)´s.
                                    # NOTA: esta variable contendrá
                                    #       el npumero de muestras
                                    #       (que en este caso serán
                                    #        500).
En_Bytes = bytearray(8000)          # Declara la variable que
                                    # contendrá el número de
                                    # muestras.
                                    # NOTA: un número en notación
                                    #       de punto flotante está
                                    #       compuesto de 4 bytes
                                    #       (32 bits).
                                    
To_CTE_A0 = bytearray(4)            # Variable receptora en ENDIAN de A0
To_CTE_A1 = bytearray(4)            # Variable receptora en ENDIAN de A1
To_CTE_A2 = bytearray(4)            # Variable receptora en ENDIAN de A2
To_CTE_B1 = bytearray(4)            # Variable receptora en ENDIAN de B1
To_CTE_B2 = bytearray(4)            # Variable receptora en ENDIAN de B2
To_FREQ   = bytearray(4)            # Variable receptora en ENDIAN de
                                    # la frecuencia a generar.



##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
##            Coeficientes de la Función de Transferencia                 ##
##          H(z) = [A0*Z^2+A1*Z+A2]/[Z^2+B1*Z+B2] = Y(z)/U(z)             ##
##                                                                        ##
##  Esto conduce a la obtención de la siguiente ecuación en diferencias:  ##
##    Y(k) = A0*U(k) + A1*U(k-1) + A2*U(k-2) - B1*Y(k-1) - B2*(k-2)       ##
##                                                                        ##
##  La asignación de constantes de programa quedaría entonces como:       ##
##            CTE_A0 = A0      CTE_A1 = A1      CTE_A2 = A2               ##
##            CTE_B1 = -B1     CTE_B2 = -B2                               ##
##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##

CTE_A0  = +0.0                       # Todas las ctes. se inicializaran en 0's.
CTE_A1  = +0.0
CTE_A2  = +0.0
CTE_B1  = +0.0
CTE_B2  = +0.0
FREQ    = 50                         # Frecuencia default es 50 HZ.
PERIODO = (1/FREQ)                   # Obten el periodo de la 
                                     # frecuencia (que es 0.02 seg y esto
                                     # equivales a 20000 uSeg).
HALF    = int((PERIODO*1000000)/2)   # Variable para obtener la mitad del valor
                                     # del periodo y posteriomente convertirla
                                     # a valores en microsegundos.

##XXXXXXXXXXXXXXXXXXXXXXXXXX##
## Condiciones Iniciales de ##
## las Entradas y Salidas.  ##
##XXXXXXXXXXXXXXXXXXXXXXXXXX##
UK     = 0.0           # u(k1)
UK1    = 0.0           # u(k-1)
UK2    = 0.0           # u(k-2)
YK     = 0.0           # y(k)
YK1    = 0.0           # y(k-1)
YK2    = 0.0           # y(k-2)
Read   = 0.0


############################################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
############################################################################################
####                                                                                    ####
####   DEFINE LA RUTINA PARA GENERAR UNA ONDA CON CUADRADA EN EL SEGUNDO NÚCLEO DE LA   ####
####   LA RASPBERRY PI PICO.                                                            ####
####   NOTA: en este caso la frecuencia esta dada como f = (1/20mSeg) = 50 Hz           ####                             ####
####                                                                                    ####
############################################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
############################################################################################

def Onda_Cuadrada():
    while True:
        Pin3.on()                             # Pon en "1" al Pin GPIO3 de laa RP2.
        sleep_us(HALF)                        # Retardo de 0.01 Seg.
        Pin3.off()                            # Pon en "0" al Pin GPIO3 de la RP2.
        sleep_us(HALF)                         # Retardo de 0.01 Seg.
        



##########################################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##########################################################################################
####                                                                                  ####
####    RUTINA PRINCIPAL QUE ES LA RESPONSABLE DE INICIAR EL "THREAD" EN 2DO PLANO    ####
####    PARA GENERAR LA ONDA CUADRADA Y LA IMPLEMENTACIÓN EN 1ER PLANO DE LA          ####
####    ECUACIÓN EN DIFERENCIAS.                                                      ####
####                                                                                  ####
####    NOTA: EL 1ER PLANO DE ESTA RUTINA IMPLEMENTA A LA ECUACIÓN EN DIFERENCIAS     ####
####          CON UNA FRECUENCIA DE MUESTREO DE 8 KHZ.                                ####
####                                                                                  ####
##########################################################################################
####XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX####
##########################################################################################

_thread.start_new_thread(Onda_Cuadrada,())  # Inicia el "thread" de la onda cuadrada.


###XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX###
###   Aquí se inicia una recepción de datos por la UART0 que está   ###
###   conectada al módulo bluetooth. El proceso es el siguiente:    ###
###                                                                 ###
###   1) Se espera una recepción inicial que tiene como 1er byte    ###
###      un identificador 0x55 que corresponde a una "U".           ###
###   2) En seguida se reciben los coeficientes A0, A1, A2, B1 y    ###
###      la frecuencia en formato ENDIAN.                           ###                                  
###   3) Se convierten a formato "float"                            ###
###   4) Se espera ahora la recepción de un caracter 0x52 que       ###
###      corresponde a una "R" y entonces comienza el proceso de    ###
###      de armado de la ecuación en diferencias, repitiéndose      ###
###      este proceso 1000 veces (para obtener 1000 iteraciones).   ###
###   5) En cada iteración se están compilando las muestras de      ###
###      entrada/salida en forma alternada. En total, se tendrán    ###
###      1000 muestras de entrada y 1000 muestras de salida, que    ###
###      dan un total de 2000 muestras.                             ###
###   6) Obsérvese que la tasa de muestreo fija es de 8 Khz.        ###
###   7) Al final de la compilación de muestras input/output se     ###
###      convertirán a formato ENDIAN para su transmisión vía       ###
###      UART0 que a su vez se mandarán por medio de la interfáz    ###
###      bluetooth.                                                 ###
###XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX###

while True:
    P25.off()                               # Apaga el Led testigo.
    
    #****************************#
    # ¿Hay algún byte pendiente? #
    #****************************#
    if UART0.any() > 0:
        LLAVE = UART0.read()                # Lee el caracter recibido o 
                                            # caracteres recibidos.
                                            
        #x x x x x x x x x x x x x x x x x x x x x x x x x #
        #  Si se recibió una "U" (o sea un 0x55 => 85),    #
        #  carga los nuevos coeficientes y la frecuencia   #
        #x x x x x x x x x x x x x x x x x x x x x x x x x #
        
        if LLAVE[0] == 0x55:
            
            ###############################################################################
            ##                                                                           ##
            ##       ADQUISICIÓN DE LOS NUEVOS COEFICIENTES CON LOS QUE TRABAJARÁ        ##
            ##       LA IMPLEMENTACIÓN ITERATIVA DE LA ECUACIÓN EN DIFERENCIAS.          ##
            ##                                                                           ##
            ###############################################################################
            
            #******************************#
            # Adquisición del ENDIAN de A0 #
            #******************************#
            To_CTE_A0[0] = LLAVE[1]
            To_CTE_A0[1] = LLAVE[2]
            To_CTE_A0[2] = LLAVE[3]
            To_CTE_A0[3] = LLAVE[4]            
                
            #******************************#
            # Adquisición del ENDIAN de A1 #
            #******************************#
            To_CTE_A1[0] = LLAVE[5]
            To_CTE_A1[1] = LLAVE[6]
            To_CTE_A1[2] = LLAVE[7]
            To_CTE_A1[3] = LLAVE[8] 
                
            #******************************#
            # Adquisición del ENDIAN de A2 #
            #******************************#
            To_CTE_A2[0] = LLAVE[9]
            To_CTE_A2[1] = LLAVE[10]
            To_CTE_A2[2] = LLAVE[11]
            To_CTE_A2[3] = LLAVE[12] 
                
            #******************************#
            # Adquisición del ENDIAN de B1 #
            #******************************#
            To_CTE_B1[0] = LLAVE[13]
            To_CTE_B1[1] = LLAVE[14]
            To_CTE_B1[2] = LLAVE[15]
            To_CTE_B1[3] = LLAVE[16] 
                
            #******************************#
            # Adquisición del ENDIAN de B2 #
            #******************************#
            To_CTE_B2[0] = LLAVE[17]
            To_CTE_B2[1] = LLAVE[18]
            To_CTE_B2[2] = LLAVE[19]
            To_CTE_B2[3] = LLAVE[20]
            
            #****************************************#
            # Adquisición de la Frecuencia a Generar #
            # (en formato ENDIAN.                    #
            #****************************************#
            To_FREQ[0] = LLAVE[21]
            To_FREQ[1] = LLAVE[22]
            To_FREQ[2] = LLAVE[23]
            To_FREQ[3] = LLAVE[24]                

            #######################################################################
            ##                                                                   ##
            ##     CONVERSIONES DE LAS CONSTANTES DE "ENDIAN" A "float" REAL     ##
            ##                                                                   ##
            #######################################################################
            
            CTE = struct.unpack('<f', bytes(To_CTE_A0))
            CTE_A0 = CTE[0]
            print("A0 = ", CTE_A0)
            CTE = struct.unpack('<f', bytes(To_CTE_A1))
            CTE_A1 = CTE[0]
            print("A1 = ", CTE_A1)
            CTE = struct.unpack('<f', bytes(To_CTE_A2))
            CTE_A2 = CTE[0]
            print("A2 = ", CTE_A2)
            CTE = struct.unpack('<f', bytes(To_CTE_B1))
            CTE_B1 = CTE[0]
            print("B1 = ", CTE_B1)
            CTE = struct.unpack('<f', bytes(To_CTE_B2))
            CTE_B2 = CTE[0]
            print("B2 = ", CTE_B2)
            
            ##############################################################
            ##   OBTENCIÓN DEL PERIODO DE LA SEÑAL PARA LA GENERACIÓN   ##
            ##   DE LA ONDA CUADRADA.                                   ##
            ##############################################################
            
            CTE     = struct.unpack('<f', bytes(To_FREQ))  # Convierte Frecuencia de
                                                           # ENDIAN a float.
            FREQ    = CTE[0]                               # Separa Frecuencia.
            PERIODO = (1/FREQ)                             # Calcula Periodo.
            HALF    = int((PERIODO*1000000)/2)             # Convierte el periodo en
                                                           # unidades de microsegundos
                                                           # divídelo entre 2 y
                                                           # conviértelo a enteros.
                                                           
        ###############################################################################
        ##   OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO    ##
        ###############################################################################
        ##                                                                           ##
        ##    Captura 500 muestras a una tasa de muestreo Fs = 8Khz provenientes     ##
        ##    de la iteraciones sucesivas de Vo(k).                                  ##
        ##    NOTA: Si paso de 500 muestras hay problemas con la memoria de la RP2.  ##
        ##                                                                           ##
        ###############################################################################
        ##   OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO  OJO    ##
        ###############################################################################
                                                           
        #x x x x x x x x x x x x x x x x x x x x x #
        #  Si se recibió una "R" (o sea un 0x52),  #
        #  ejecuta el programa de la H(z)..        #
        #x x x x x x x x x x x x x x x x x x x x x #
            
        if LLAVE[0] == 0x52:
            P25.on()                        # Led Testigo de Actividad.
            
            for i in range(0,500):         # Ciclo para 500 muestras.
                
                #* * * * * * * * * * * * * * * * * * * * #
                #  Armado de la ecuación en diferencias  #
                #* * * * * * * * * * * * * * * * * * * * #
                
                YK = CTE_A0*UK+CTE_A1*UK1+CTE_A2*UK2+CTE_B1*YK1+CTE_B2*YK2
                
                #x x x x x x x x x x x x x x x x x x x x x x#
                #  Actualiza I/O para la próxima iteración  #
                #x x x x x x x x x x x x x x x x x x x x x x#
                
                UK2 = UK1                                    # U(k-1) ----> U(k-2)           
                UK1 = UK                                     # U(k)   ----> U(k-1)
                YK2 = YK1                                    # Y(k-1) ----> U(k-2)
                YK1 = YK                                     # Y(k)   ----> Y(k-1)
                
                Read = ADC0.read_u16() * conversion_factor   # Toma lectura del canal 0
                                                             # del ADC en volts reales.
                UK = Read                                    # Asigna el nuevo valor U(k).
                ENTRADAS[i] = UK                             # Compila las entradas.
                SALIDAS[i]  = YK                             # Compila las salidas.
                sleep_us(66)                                 # Retardo de 125 uSeg.
                                                             # OJO  OJO  OJO  OJO  OJO
                
                
            P25.off()                                        # Apaga Led Testigo
                

            ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ##
            ##  Compilación Inicial de Entradas y Salidas a formato ENDIAN.  ##
            ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ##
            
            En_Bytes  = bytearray(struct.pack("f",ENTRADAS[0])) 
            En_Bytes  = En_Bytes + bytearray(struct.pack("f",SALIDAS[0]))
            
            for k in range(1,500):
                
                #x x x x x x x x x x x x x x x x x x x x x x x x x x x x #
                #  Agregado de muestras subsecuentes en formato ENDIAN.  #
                #x x x x x x x x x x x x x x x x x x x x x x x x x x x x #
                
                En_Bytes = En_Bytes + bytearray(struct.pack("f", ENTRADAS[k]))
                En_Bytes = En_Bytes + bytearray(struct.pack("f", SALIDAS[k]))
                
            ## * * * * * * * * * * * * * * * * * * * * * * * * * * * ##
            ##   Transmisión de las Entradas y Salidas por la UART0  ##
            ## * * * * * * * * * * * * * * * * * * * * * * * * * * * ##
                
            UART0.write(En_Bytes)
            En_Bytes = bytearray()
            
            ##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
            ## NOTA MUY IMPORTANTE: Si no se hacía este intercalado de entradas/salidas, ##
            ## se observó que se presentaba un corrimiento en frecuencia indeseable al   ##
            ## desplegar las señales en el paquete MATLAB.                               ##
            ##XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX##
