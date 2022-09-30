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
from gaiaClasses import *
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


async def sigils(ctx, phrase, colorsIn, altFlip, layout, randcolor, lines, nonalternating):

    #### Deal with arguments
    ##                                     altFlip stuff
    if (altFlip):
        startAlt = 1
    else:
        startAlt = -1
    alt = startAlt

    if(nonalternating):
        alternating = False
    else:
        alternating = True
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
        distDivide = distDivideStart
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
            if (str(words[m][k]) in key):## make sure it's in the key ##todo include key in layout
                safePrompt = safePrompt + words[m][k]##add it to the safePrompt
        if(safePrompt!=''):
            safeWords.append(safePrompt)##add that phrase into safeWords
    print(safeWords)

    wordSymbols = [] ## holds all the word symbols

    for u in range(len(safeWords)):##go through all the words
        wordSymbols.append(wordSymbol(safeWords[u])) ## create a new wordSymbol with this word
        if(len(safeWords[u])==1):## if it's a one letter word, put it on the circle list (check not empty)
            letter = safeWords[u][0] ##get the letter
            points = circlePoints(layout[letter], circleRadius) ## get the points for that letter
            wordSymbols[u].setCircle(points)
        elif(len(safeWords[u])>1):
            connectionList = []
            for x in range(len(safeWords[u])-1): ##loop through that word and add the letter connections to the array
                connectionList.append(connection(layout, safeWords[u][x], safeWords[u][x+1]))
            print(f'connectionList: {connectionList}')
            wordSymbols[u].setConnections(connectionList) ## add connections to the wordSymbol
            wordSymbols[u].setCircle(circlePoints(layout[safeWords[u][0]], circleRadius)) ## add first circle to wordSymbol
            wordSymbols[u].conToPath(globalOffset, distDivide, startAlt, alternating) ## turn the connection list into a path


    ############## Draw everything
    for s in range(len(wordSymbols)): ##loop through all wordSymbols
        symbolCurrent = wordSymbols[s] # set current wordSymbol
        ## set pens
        outlinePen = aggdraw.Pen(outlineColor, stroke+outlinePX)##set outline pen
        pen = aggdraw.Pen(colors[colorCount], stroke)##set pen color
        circleFill = aggdraw.Brush(colors[colorCount])
        if (colorCount<numColors):
            colorCount +=1

        ## draw outlines
        if(symbolCurrent.pathed): # if there is a path to draw
            draw.symbol((0,0), symbolCurrent.retSymbol(), outlinePen)##draw it
        draw.ellipse(symbolCurrent.circle[0], outlinePen, circleOutline)##draw the circle outline
        draw.flush()

        ## draw colored bits
        if (symbolCurrent.pathed):
            draw.symbol((0,0),symbolCurrent.retSymbol(), pen)##draw it
        draw.ellipse(symbolCurrent.circle[0], pen, circleFill)##draw them
        draw.flush()

    ####

    ## do the saving
    finPrompt = " ".join(safeWords)
    saveFile=vaultPath + f"{finPrompt}-sigil.png"
    print (f"Saving {saveFile}")
    print ("##################")
    back.save(saveFile)
    return saveFile
