import numpy

def colour(h):     #Colour is between 0 and 360
    
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

def hex_colour(h, dilution = 1):

    col = colour(h)
    col = (int((col[0]*255)*dilution + 255*(1 - dilution)), int((col[1]*255)*dilution + 255*(1 - dilution)), int((col[2]*255)*dilution + 255*(1 - dilution)))
    return '#%02x%02x%02x' % col

def gcd(a, b):    #GCD of two numbers
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

def lcm(lis):
    if len(lis) == 1:
        return lis[0]
    else:
        l = lcm(lis[:-1])
        return int(lis[-1]*l/gcd(lis[-1], l))
    
from tkinter import *
from math import cos, sin, pi, floor
from time import sleep
import pygame.midi

beats = [7,11]#[2,3,4,5,6,10,12,15,20,30,60]
beats.reverse()
radii = list(numpy.linspace(0,400,len(beats)+1))
steps = 0
instrument = 48#52
notes = [31+30,36+30]#[0,4,7,12,16,19,24,28,31,36,40]
volume = 150
l = lcm(beats)
tempo = 40
playing = True

def main():

    root =  Tk()
    root.title("pOLyRHYthMon")
    canvas = Canvas(root, width = 2*radii[-1], height = 2*radii[-1], bg = "#ffffff")
    canvas.pack()

    """pygame.midi.init()
    instruments = []
    for i in range(len(notes)):
        instruments.append(pygame.midi.Output(i))
        instruments[-1].set_instrument(notes[i][0], i)"""

    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(instrument, 1)

    def box(i):
        return radii[-1] - radii[- i], radii[-1] - radii[- i], radii[-1] + radii[- i], radii[-1] + radii[- i]
    
    def draw_bg(c, k):                               #Draws the gratings and text widget (with the basis in red only showing if basis_show is set to true)
        c.delete("all")
        playingq = [False]*len(beats)
        for i in range(len(beats)):
            step = floor(beats[i]*k/l)%beats[i]
            if beats[i]*k%l == 0:   #New beat:
                playingq[i] = True
                #print(k)
            for j in range(beats[i]):
                if j == step:
                    c.create_arc(*box(i + 1), start = -360*j/beats[i] + 90, extent = -360/beats[i], fill = hex_colour(360*i/(len(radii)), dilution = 1/5), width = 3)
                else:
                    c.create_arc(*box(i + 1), start = -360*j/beats[i] + 90, extent = -360/beats[i], fill = hex_colour(360*i/(len(radii))), width = 3)  #Angles just don't line up.
        c.create_oval(*box(0), fill = "#ffffff", width = 3)
        for i in range(len(beats)):
            if playingq[i]:
                player.note_on(notes[i], 127, 1)
        sleep(60/(tempo*l))
        for i in range(len(beats)):
            if playingq[i]:
                player.note_off(notes[i], 127, 1) 
        
    global steps
    
    while True:
        if playing:
            steps += 1
            draw_bg(canvas, steps)
            root.update()
            #sleep(60/(tempo*l))

    root.mainloop()

if __name__ == "__main__":
    main()
    
##http://www.pygame.org/docs/ref/midi.html for midi files

