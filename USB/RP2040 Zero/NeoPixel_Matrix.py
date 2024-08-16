# Waveshare RP2040-MATRIX with 5x5 grid of Neopixels
#### Usando coordenadas: valores (x, y) o (col, row)

# NB colours (green, red, blue)
# Tony Goodhew for the pihut.com - 25 Aug 2023
import time
from machine import Pin
from neopixel import NeoPixel

# Set up 25 Neopixels on GPIO 16
np = NeoPixel(Pin(16), 25, bpp = 3) # bpp = bytes per pixel (GRB)

def clear():
    np.fill((0,0,0))
    np.write()
    
def wait(t):            # Delay t seconds
    time.sleep(t)
   
for i in range(25):  # 'Natural' order 0-24, as connected on board  
    np[i] = (10,10,0)   # Yellow ON
    np.write()
    wait(0.15)
    np[i] = (0,0,0)     # Black OFF - Single blink
    wait(0.2)

clear()
wait(0.6)

for row in range(5): # Row at a time
    for col in range(5):
        np[5 * row + col] = (5,5,5) # White
        np.write()
        wait(0.15)
    wait(0.1)
clear()

for col in range(5): # Column at a time
    for row in range(5):
        np[5 * row + col] = (0,0,5) # Blue
        np.write()
        wait(0.15)
    wait(0.2)
clear()

def sq(x,y,n,r,g,b):
    for col in range(x,x+n):  # Top and Bottom
        np[5 * y + col] = (g,r,b) 
        np[5 * (y+n-1) + col] = (g,r,b)

    for row in range(y,y+n):  # Sides
        np[5 * row + x] = (g,r,b) 
        np[5 * row + x + n -1] = (g,r,b)    
    np.write()

tt = 0.6
sq(0,0,5,4,0,0)
wait(tt)
sq(0,0,4,0,4,0)
wait(tt)
sq(0,0,3,0,0,4)
wait(tt)
sq (0,0,2,4,4,0)
wait(tt)
sq(0,0,1,0,4,4)
wait(tt)
clear()
