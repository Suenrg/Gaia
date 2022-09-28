##variableSigils.py Bea Shakow 9/25/2022
import os
from PIL import Image, ImageDraw, ImageFont
import shelve
import aggdraw
import numpy as np
from connection import *



key = "abcdefghijklmnopqrstuvwxyz1234567890".upper()
filePath="layouts.txt"
fontSize = 100
canX = 600
canY = 600
leng = fontSize
lineWidth = 10
layout = {}
colors = ["#4324AD", "#4D83FA", "#8734FA"]
stroke = 10
globalOffset = 1
alt = -1
alternating = True



path = os.path.dirname(__file__)+"\\images\\"
back = Image.open(path+"blank.png")
draw = aggdraw.Draw(back)
outline = aggdraw.Pen(colors[0], stroke) # 5 is the outlinewidth in pixels

with shelve.open(filePath, writeback=False) as f:
    layout = f["rect"]


prompt="one h"
prompt=prompt.upper()
words = prompt.split(" ")
print(words)
safeWords = []

for m in range(len(words)):
    safePrompt = ""
    for k in range(len(words[m])):
        if (str(words[m][k]) in key):
            #print(words[m][k])
            safePrompt = safePrompt + words[m][k]
    safeWords.append(safePrompt)

#print (safeWords)

conList = [] ## list of lists of connections, list for each word's connections in a list
circleList = [] ## list of circles to do

Fletter = safeWords[0][0]
circleList.append([layout[Fletter][0]-leng/4,layout[Fletter][1]-leng/3,(layout[Fletter][0]-leng/4)+leng/2,(layout[Fletter][1]-leng/3)+leng/2])
for u in range(len(safeWords)):
    conList.append([])

    if(len(safeWords[u])==1):
        print("only one")
        letter = safeWords[u][0]
        print(letter)
        topLeftX = layout[letter][0]-leng/4
        topLeftY = layout[letter][1]-leng/3
        botRightX = topLeftX + leng/2
        botRightY = topLeftY + leng/2
        circleList.append([topLeftX, topLeftY, botRightX, botRightY])
    else:
        for x in range(len(safeWords[u])-1):
            conList[u].append(connection(layout, safeWords[u][x], safeWords[u][x+1]))

print(circleList)

# for p in conList:
#     for t in p:
#         t.prints()
#     print("next word:")





strings = []
for e in range(len(conList)): ## loop through the word connection lists conList[e] is word #e's list of connections
    newString = ""
    for i in range(len(conList[e])): ##loop through each connection in this word's connection list
        current = conList[e][i]
        #current.prints()
        if(i==0):
            newString = f'M{current.aPT()} Q{current.controlPoint(globalOffset, alt)}, {current.bPT()} '
            if(alternating):
                alt = alt * -1
        else:
            newString = newString + f'{current.controlPoint(globalOffset, alt)}, {current.bPT()} '
            if(alternating):
                alt = alt * -1
    strings.append(newString)

print(strings)


symbols = []
for j in range(len(strings)):
    symbols.append(aggdraw.Symbol(strings[j]))
# xy = layout[prompt[0]]
for y in range(len(symbols)):
    outline = aggdraw.Pen(colors[y], stroke)
    draw.symbol((0,0),symbols[y], outline)
    draw.flush()

for h in range(len(circleList)):
    draw.ellipse(circleList[h], outline)
    draw.flush()

back.show()
