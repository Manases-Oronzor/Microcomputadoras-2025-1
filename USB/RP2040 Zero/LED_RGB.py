import machine
#from neopixel import Neopixel
import neopixel
from time import sleep

pixel_pin = 16

# Crea un objeto LED de la clase Neopixel en el Pin 16

#led = Neopixel(machine,Pin(16,1))
led = neopixel.NeoPixel(machine.Pin(16),1)

while (True):
    # ROJO
    led[0] = (255, 0, 0)
    led.write()
    sleep(0.25)
    
    # VERDE
#    led[0] = (0, 128, 0)
    led[0] = (0, 255, 0)
    led.write()
    sleep(0.25)
    
    # AZUL
#    led[0] = (0, 0, 64)
    led[0] = (0, 0, 255)
    led.write()
    sleep(0.25)
    
    
    led[0] = (255, 200, 0)
    led.write()
    sleep(0.25)
    
    led[0] = (255, 0, 255)
    led.write()
    sleep(0.25)
    
    led[0] = (0, 255, 255)
    led.write()
    sleep(0.25)