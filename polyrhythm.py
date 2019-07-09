###A striking polyrhythm visualiser in Python using Tkinter and PyGame
###Made by OrigamiDrag0n, 07/07/19 - 09/07/19
###Large lowest common divisors may take a long time to process, so do be aware.
###Requires PyGame and NumPy packages

###Graphics###

def colour(h):                               #Hue to RGB colour (from 1 to 360)
    
    if h < 60:
        return (1, 1-abs(h/60%2 -1) ,0)
    elif h < 120:
        return (1-abs(h/60%2 -1),1,0)
    elif h < 180:
        return (0,1,1-abs(h/60%2 -1))
    elif h < 240:
        return (0,1-abs(h/60%2 -1),1)
    elif h < 300:
        return (1-abs(h/60%2 -1),0,1)
    else:
        return (1,0,1-abs(h/60%2 -1))

def hex_colour(h, dilution = 1):       #Turns a hue colour with a given dilution into a hexadecimal value

    col = colour(h)
    col = (int((col[0]*255)*dilution + 255*(1 - dilution)), int((col[1]*255)*dilution + 255*(1 - dilution)), int((col[2]*255)*dilution + 255*(1 - dilution)))
    return '#%02x%02x%02x' % col


###Number theory###

def gcd(a, b):                                         #GCD of two numbers
    
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

def lcm(lis):                                          #Lowest common multiple of a list of numbers
    
    if len(lis) == 1:
        return lis[0]
    else:
        l = lcm(lis[:-1])
        return int(lis[-1]*l/gcd(lis[-1], l))
    
###The modules###

from tkinter import *
from math import cos, sin, pi, floor
from time import sleep
import pygame.midi
from numpy import linspace

###The mainloop###

beats = [2,3,4,5,6,10,12,15,20,30,60]                  #The individual rhythms (number of beats per rotation)
radii = list(numpy.linspace(0,400,len(beats)+1))       #Radii of the circles
steps = 0                                              #Initial rotation (relative to the lcm of the beats)
instrument = 52                                        #Midi instrument number
notes = [0,4,7,12,16,19,24,28,31,36,40]                #Note values 
l = lcm(beats)                                         #Smallest increment (lowest common multiple of all the beats)
tempo = 40                                             #Rotations per minute

def main():

    root =  Tk()
    root.title("pOLyRHYthM")
    canvas = Canvas(root, width = 2*radii[-1], height = 2*radii[-1], bg = "#ffffff")
    canvas.pack()

    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(instrument, 1)

    def box(i):                                        #Box dimensions
        return radii[-1] - radii[- i], radii[-1] - radii[- i], radii[-1] + radii[- i], radii[-1] + radii[- i]
    
    def draw_bg(c, k):                                 #Draws the diagram on the canvas, and plays the appropriate noises
        c.delete("all")
        playingq = [False]*len(beats)
        for i in range(len(beats)):
            step = floor(beats[i]*k/l)%beats[i]        #Which section is being played at that moment
            if beats[i]*k%l == 0:                      #New beat occurs, and is stored
                playingq[i] = True
            for j in range(beats[i]):                  #Draws the diagram
                if j == step:
                    c.create_arc(*box(i + 1), start = -360*j/beats[i] + 90, extent = -360/beats[i], fill = hex_colour(360*i/(len(radii)), dilution = 1/5), width = 3)
                else:
                    c.create_arc(*box(i + 1), start = -360*j/beats[i] + 90, extent = -360/beats[i], fill = hex_colour(360*i/(len(radii))), width = 3)  #Angles just don't line up.
        c.create_oval(*box(0), fill = "#ffffff", width = 3)
        for i in range(len(beats)):                    #Playing all the notes
            if playingq[i]:
                player.note_on(notes[i], 127, 1)
        sleep(60/(tempo*l))
        for i in range(len(beats)):
            if playingq[i]:
                player.note_off(notes[i], 127, 1) 
        
    global steps
    
    while True:                                         #Main loop
        if playing:
            steps += 1
            draw_bg(canvas, steps)
            root.update()

    root.mainloop()

if __name__ == "__main__":
    main()
    
