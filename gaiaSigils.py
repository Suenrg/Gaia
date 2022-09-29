## gaiaSigils.py bea shakow 2022
import os
import sys
import random
import asyncio
import shelve
import os
from PIL import Image, ImageDraw, ImageFont
import shelve
import aggdraw
import numpy as np
from connection import *
from funcs_sigil import *

#### variables
key = "abcdefghijklmnopqrstuvwxyz1234567890".upper()
filePath="layouts.txt"
path = os.path.dirname(__file__)+"\\images\\"
vaultPath = os.path.dirname(__file__)+"\\vault\\"

fontSize = 100
numColors = 10
canX = 600
canY = 600
leng = fontSize
layout = {}


##editable
stroke = 10
outlinePX = 10
outlineColor = "#000000"#"#963C2C"
circleRadius = 15
globalOffsetStart = 50
distDivideStart = 100
startAlt = -1
alt = -1
alternating = True
background = path+"blank.png"
layoutPath = "spiral"

####


async def sigils(ctx, phrase, colorsIn, altFlip, layout, randcolor, lines):

    #### Deal with arguments
    ##                                     altFlip stuff
    if (altFlip):
        startAlt = 1
    else:
        startAlt = -1
    alt = startAlt
    ##                                     color stuff
    colors = []
    colorsIn = colorsIn.split(",")
    print(colorsIn)
    for x in range(len(colorsIn)):
        colors.append(colorsIn[x].strip())
    ##                                     layout
    layoutPath=layout
    ##                                     randcolor
    if (randcolor and colors[0]=="#4324AD"):
        colors=[]
        for i in range(numColors):
            colors.append(randomColor())
    ##                                     straight lines or not?
    if (lines):
        globalOffset = 1
    else:
        globalOffset = globalOffsetStart
        distDivide = distDivideStart
    ####

    ####

    #### args print test
    print(f'with startAlt:{startAlt}, colors:{colors}, layout:{layoutPath}')

    ## open the image
    back = Image.open(background)
    draw = aggdraw.Draw(back)

    ## set up the pen and brush
    pen = aggdraw.Pen(colors[0], stroke)
    circleFill = aggdraw.Brush(colors[0])
    circleOutline = aggdraw.Brush(outlineColor)
    colorCount = 0



    ##load the layout
    with shelve.open(filePath, writeback=False) as f:
        layout = f[layoutPath]
    ##sanitize prompt
    prompt=phrase.upper()
    words = prompt.split(" ")

    safeWords = [] ## holds the sanitized words
    for m in range(len(words)): ##go through each word
        safePrompt = ""
        for k in range(len(words[m])):##go through each letter of the word
            if (str(words[m][k]) in key):## make sure it's in the key
                safePrompt = safePrompt + words[m][k]##add it to the safePrompt
        if(safePrompt!=''):
            safeWords.append(safePrompt)##add that phrase into safeWords
    print(safeWords)

    conList = [] ## list of lists of connections, list for each word's connections in a list
    circleList = [] ## list of circles to do
    circleOutlineList = [] # list of circle outlines to do

    for u in range(len(safeWords)):##go through all the words
        if(len(safeWords[u])==1):## if it's a one letter word, put it on the circle list (check not empty)
            conList.append([]) ## fill the space in conList so U  keeps track
            letter = safeWords[u][0] ##get the letter
            points = circlePoints(layout[letter], circleRadius)
            circleList.append(points) ## put them on the circleList
            circleOutlineList.append(points)
        elif(safeWords[u]):
            conList.append([]) ##make a new list in conlist for a new word
            for x in range(len(safeWords[u])-1): ##loop through that word and add the letter connections to the array
                conList[u].append(connection(layout, safeWords[u][x], safeWords[u][x+1]))

    ## set up each path string asd asd
    strings = [] ##holds all the path strings
    for e in range(len(conList)): ## loop through the word connection lists conList[e] is word #e's list of connections
        newString = "" ## new pathstring for each word
        alt = startAlt
        for i in range(len(conList[e])): ##loop through each connection in this word's connection list
            current = conList[e][i] #set current connection
            if(i==0): ## if it's the beginning
                newString = f'M{current.aPT()} Q{current.controlPoint(globalOffset, distDivide, alt)}, {current.bPT()} '
                points = circlePoints(layout[current.a], circleRadius)
                circleList.append(points) ## put them on the circleList
                if(alternating):
                    alt = alt * -1
            else: ##otherwise just add
                newString = newString + f'{current.controlPoint(globalOffset, distDivide, alt)}, {current.bPT()} '
                if(alternating):
                    alt = alt * -1
        strings.append(newString) ##add our new string to strings

    symbols = [] ## list for all the bezier curve symbols
    for j in range(len(strings)):##go through strings
        symbols.append(aggdraw.Symbol(strings[j]))##add a symbol for each word

    ############## Draw everything

    for y in range(len(symbols)):##draw outline before
        outline2 = aggdraw.Pen(outlineColor, stroke+outlinePX)##draw outline
        draw.symbol((0,0),symbols[y], outline2)##draw it
        draw.flush()

    for h in range(len(circleList)):## draw circle outlines
        draw.ellipse(circleList[h], outline2, circleOutline)##draw them
        draw.flush()

    for y in range(len(symbols)):##draw all symbols
        pen = aggdraw.Pen(colors[colorCount], stroke)##change pen color
        if (colorCount<numColors):
            colorCount +=1
        draw.symbol((0,0),symbols[y], pen)##draw it
        draw.flush()

    colorCount = 0
    for h in range(len(circleList)):## go through all the circles we need
        pen = aggdraw.Pen(colors[colorCount], stroke)##change pen color
        circleFill = aggdraw.Brush(colors[colorCount])
        if (colorCount<numColors):
            colorCount +=1
        draw.ellipse(circleList[h], pen, circleFill)##draw them
        draw.flush()


    finPrompt = " ".join(safeWords)
    saveFile=vaultPath + f"{finPrompt}-sigil.png"
    print (f"Saving {saveFile}")
    print ("##################")
    back.save(saveFile)
    return saveFile
