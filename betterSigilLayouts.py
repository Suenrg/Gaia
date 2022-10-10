import os
import shelve
import numpy as np
from tkinter import *
from tkinter import ttk
from conf import *
from funcs_sigil import *


path = os.path.dirname(__file__)+"\\images\\"


filePath="layouts.txt"
fontSize = 100
canX = 600
canY = 600
leng = fontSize
startX = leng/2
startY = leng/2+10
lineWidth = 10
layout={}
sigilName = 'geomabet'
radius = 15

c = 0
##Tkinter setup
win = Tk()
win.title('Sigil Layout Creator')
win.geometry(f"{canX}x{canY}")

background = PhotoImage(file = (path+"aly_layout.png"))

canvas = Canvas(win, width=canX, height=canY)
canvas.pack()

canvas.create_image(
    0,
    0,
    anchor=NW,
    image=background
    )
# Label(win,image=background).pack()

## set up the set into a list
set="abcdefghijklmnopqrstuvwxyz".upper()
list = []
for i in set:
    list.append(i)



def click_handler(event):
    global c
    if event.num == 1:
        pos = (event.x, event.y)
        layout[list[c]] = pos
        print(f'{list[c]}, {pos}')
        print(f'{layout}')
        c += 1
        points=circlePoints(pos, radius)
        canvas.create_oval(points[0],points[1],points[2],points[3],fill="red")

def save_handler(event):
    with shelve.open(layoutsPath, writeback=True) as f:
        print ('saved!')
        f[sigilName]=layout


win.bind("<Button 1>", click_handler)
win.bind("<Button 2>", save_handler)

win.mainloop()
