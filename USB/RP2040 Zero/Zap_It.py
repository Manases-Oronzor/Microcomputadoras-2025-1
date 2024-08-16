# WS RP2040 'Zap it' Game
# Needs a button switch between GPIO 14 and GND
# Tony Goodhew 28th Aug 2023 (Author)
# How to play:
#   A white target runs round the edge of the display.
#   The player starts with 100 points and tries zap the target while it is
#   to the right of the red target marker.
#   If the player hits the button too early, too late or misses a rotation
#   past the target position a point is lost.
#   A hit is registered with the target turning yellow and a green pixel is lit.
#   A point lost is indicated by a short blue flash.
#   The score is shown at the end of the go.

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

# =========== START OF FONT LIBRARY ===========
# Instructions:
# display(n,rr,gg,bb) # (ASCII value, red, green, blue)  = stationary character
# scroll(s,rr,gg,bb)  # (string, red, green, blue) = Scrolled message

# Character codes ASCII 32 - 127 5x5 pixels
# 5x5 font - Tony Goodhew 26th August 2023 (author)
# 5 columns of 5 bits = LSBs [@ == 00000]
q = [
    "@@@@@", #    32
    "@@]@@", #  ! 33
    "@X@X@", #  " 34
    "J_J_J", #  # 35
    "IU_UR", #  $ 36
    "QBDHQ", #  % 37
    "JUJA@", #  & 38
    "@@X@@", #  ' 39
    "@NQ@@", #  ( 40
    "@@QN@", #  ) 41
    "@J~J@", #  * 42
    "@DND@", #  + 43
    "@@BC@", #  , 44
    "@DDD@", #  - 45
    "@@A@@", #  . 46
    "ABDHP", #  / 47
    "NQQN@", #  0 48
    "@I_A@", #  1 49
    "IS_I@", #  2 50
    "UUUJ@", #  3 51
    "^BGB@", #  4 52
    "]UUR@", #  5 53
    "NUUF@", #  6 54
    "PSTX@", #  7 55
    "JUUJ@", #  8 56
    "LUUN@", #  9 57
    "@@E@@", #  : 58
    "@@BC@", #  ; 59
    "DJQ@@", #  < 60
    "@JJJ@", #  = 61
    "@QJD@", #  > 62
    "HPUH@", #  ? 63
    "_QUU]", #  @ 64
    "OTTO@", #  A 65
    "_UUJ@", #  B 66
    "NQQQ@", #  C 67
    "_QQN@", #  D 68
    "_UUQ@", #  E 69
    "_TTP@", #  F 70
    "NQUV@", #  G 71
    "_DD_@", #  H 72
    "@@_@@", #  I 73
    "BAA^@", #  J 74
    "_DJQ@", #  K 75
    "_AAA@", #  L 76
    "_HDH_", #  M 77
    "_HD_@", #  N 78
    "NQQN@", #  O 79
    "_TTH@", #  P 80
    "NQSO@", #  Q 81
    "_TVI@", #  R 82
    "IUUR@", #  S 83
    "PP_PP", #  T 84
    "^AA^@", #  U 85
    "XFAFX", #  V 86
    "~C~C~", #  W 87
    "QJDJQ", #  X 88
    "PHGHP", #  Y 89
    "QSUY@", #  Z 90
    "@_Q@@", #  [ 91
    "PHDBA", #  \ 92
    "@Q_@@", #  ] 93
    "@HPH@", #  ^ 94
    "AAAA@", #  _ 95
    "@@X@@", #  ` 96
    "BUUO@", #  a 97
    "_EEB@", #  b 98
    "FIII@", #  c 99
    "BEE_@", #  d 100
    "NUUH@", #  e 101
    "@_TP@", #  f 102
    "HUUN@", #  g 103
    "@_DG@", #  h 104
    "@@W@@", #  i 105
    "@AAV@", #  j 106
    "_DJA@", #  k 107
    "@_A@@", #  l 108
    "OHDHO", #  m 109
    "@GDG@", #  n 110
    "FIIF@", #  o 111
    "OJJD@", #  p 112
    "DJJG@", #  q 113
    "OHHD@", #  r 114
    "IUUR@", #  s 115
    "@H_I@", #  t 116
    "NAAN@", #  u 117
    "HFAFH", #  v 118
    "LCLCL", #  w 119
    "@JDJ@", #  x 120
    "@LEO@", #  y 121
    "@KMI@", #  z 122
    "@DNQ@", #  { 123
    "@_@@@", #  | 124
    "@QND@", #  } 125
    "HPHP@", #  ~ 126
    "@HTH@", #   127
    ]

# This procedure converts the font codes to a string
# of 25 ones and zeros characters - 5 cols of 5 rows
def decode(qq):
    powers = [16,8,4,2,1]
    str25 = ""
    for p in range(5):
        n = ord(qq[p])
        if n == 126:
            n = 92 # replace ~ with \
        str5 = ""
        for c in range(5):
            if ((powers[c] & n)/powers[c]) == 1:
                str5 = str5 + "1"
            else:
                str5 = str5 + "0"
        str25 = str25 + str5
    return str25  

# Display a single character
def display(n,rr,gg,bb): # ASCII value, red, green blue    
    qq = decode(q[n])    # get coded character pattern    
    clear()              # Clear the display to BLACK
    for c in range(5):      # Loop through the 5 columns
        for r in range(5):  # Loop through the rows
            cc = qq[r + 5 * c] # current 'bit' at (c, r) coordinate
            if cc == "1":      # Is current 'bit' a one?
                np[5 * r + c] = (gg,rr,bb) # If so, set to colour
    np.write()  # Update the display   

# Display a 'frame' of 25 bits - Used in scroll
def display_frame(ss,rr,gg,bb): # Message string of chars and colour
    clear()
    for c in range(5):          # Columns
        for r in range(5):      # Rows
            cc = ss[r + 5 * c]  # Get the 'bit' at (c,r)
            if cc == "1":       # Is it a one?
                np[5 * r + c] = (gg,rr,bb) # If so, set to colour
    np.write()          # Update display
    
def scroll(s,rr,gg,bb):
    long = ""
    s = " " + s + "  "           # Add a space character at the end
    l = len(s)                   # Length of string
    for p in range(l):           # Loop through the characters
        i = ord(s[p])-32         # Adjusted ASCII No of character
        temp = decode(q[i])      # get coded character code
        long = long + temp       # Concatenate char to long string
        last5 = temp[-5:]        # Get last 5 characters
        if last5 != "00000":     # Is there a "1" in last column?
            long = long +"00000" #   If so, add an extra space column (W and M are wider)
            
    # We now have a very long string of ones and zeros to send to
    # the display in small 'frames' of 25 bits each to fill the pixels
    
    p = 0
#    print(s," Buffer: ",len(long))
    while p < len(long)-25:           # Have we reached the end?
        frame = long[p:p + 25]        # Extract the 'frame' of 25 bits
        display_frame(frame,rr,gg,bb) # Show the frame on the Neopixels
        p = p + 5                     # Move pointer forward by 1 column
        wait(0.17)                    # Short delay - reduce to speed up scrolling
# ========== END OF FONT LIBRARY =============

# ======= MAIN ===================
sw = Pin(14, Pin.IN,Pin.PULL_UP)      # Set up button - Zero when pressed
# Title
scroll("Zap it",5,5,0)
clear()
np.write()
score = 0            # Targets zapped!
opps = 0             # Zap opportunities = pass the target area
p = 0                # Position of target on circuit (0-15)
errors = 0
err = 0
running = True       # Loop control variable
loops = 4000         # Delay loop variable - reduce to increase speed - harder!
route = [10,5,0,1,2,3,4,9,14,19,24,23,22,21,20,15] # By pixel numbers
p = 0
err = 0
while score < 3:     # You have 3 goes
    running = True
    display(17 + score,0,0,5) # Display the 'Go' number - 1 to 3
    np.write()
    time.sleep(0.3)
    clear()
    np[13] = (0,5,0)     # Display Red 'Target marker'
    if score > 0:
        np[6] = (3,0,0)
    if score == 2:
        np[7] =(3,0,0)        
    np.write
    while running:
        np[route[p]] = (3,3,3) # White target
        np.write()
        for w in range(loops):                           
            if sw.value() == 0:            # Read switch
                if p != 8 :                # Off target ?
                    # Missed! - too early or too late
                    err = 1                # Increment errors
                    np[16] = (0,0,5)       # Err Flag set - blue
                    np.write()
                if (p == 8) and (err == 0):# On target?
                    # Zapped!
                    w = loops+10 #         # Halt w loop
                    running = False        # Halt outer loop
                    np[14] = (5,5,0)       # Hit flag set  = yellow
                    score = score + 1           # Increment score
                    np[score + 5] = (3,0,0)     # Hit score incremented - green
                    np.write()
                    time.sleep(1)
        if p == 8:
            opps = opps + 1                # Increment opportunities counter       
        np[route[p]] = (0,0,0)             # Clear current target position
        np.write()
        p = (p + 1) % 16                   # Increment loop pointer
        if p == 0:
            errors = errors + err          # Update errors
            err = 0
            np[16] = (0,0,0)               # Turn off blue err flag
    
    np.write()

print(score, opps, errors)
result = 103 - opps - errors
print(result)
scroll("Score: " + str(result),5,5,0)
