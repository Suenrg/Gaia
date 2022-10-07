## async_connection.py bea Shakow 2022

import numpy as np
import math
import aggdraw

class connection: ## Holds a connection between two words
    def __init__(self, layout, a, b):
        self.a = a
        self.b = b
        self.layout = layout

    def compare(self, other):
        if ((self.a==other.a) and (self.b == other.b)):
            return True
        elif ((self.a==other.b) and (self.b==other.a)):
            return True
        else:
            return False

    def aPT(self):
        return f'{self.layout[self.a][0]}, {self.layout[self.a][1]}'
    def bPT(self):
        return f'{self.layout[self.b][0]}, {self.layout[self.b][1]}'

    def controlPoint(self, offset, distDivide, alt):
        ## control point math
        x1 = self.layout[self.a][0]
        y1 = self.layout[self.a][1]
        x2 = self.layout[self.b][0]
        y2 = self.layout[self.b][1]
        ##find midpoint
        x3=(x1+x2)/2
        y3=(y1+y2)/2

        #print(f'x3:{x3},    y3:{y3}')
        ##find slope
        dX = x2-x1
        dY = y2-y1
        if(dX==0):
            dX=.001
        #print(f'dX:{dX},    dY:{dY}')
        slope = dY/dX

        ##line equation is y-y3=-(1/m)(x-x3), y=-1/m(x-x3)+y3, x=(y-y3)
        ##slope for vector should be -(1/slope)
        x4 = x3+70
        if ((-slope)==0):
            slope=-.001
        y4 =(offset/(-slope))+y3

        ## do we alt?
        vec = np.array([x4-x3, y4-y3])
        vec = vec*alt

        #print(vec)
        unit_vec = vec / (vec**2).sum()**0.5
        #print(unit_vec)
        dist = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
        final_vec = unit_vec*(offset*(dist/distDivide))
        #print(final_vec)
        nX = int(x3 + final_vec[0])
        nY = int(y3 + final_vec[1])

        if (nX >= 600): #keep control points on screen
            nX = 600
        if (nY >= 600):
            nY = 600
        if (nX <= 0):
            nX = 0
        if (nY <= 0):
            nY = 0
        #print(f'nX: {nX},   nY: {nY}')
        return f'{nX}, {nY}'

    def prints(self):
        print(f'a = {self.a}: {self.layout[self.a]} ; b = {self.b}: {self.layout[self.b]}')

class wordSymbol(): ## holds the symbol and circles and lines for each word
    def __init__(self, wordIN):
        self.word = wordIN
        self.pathString = ""
        self.circle = []
        self.connections = []
        self.pathed = False
        self.line = []
        self.lastAlt = 1

    def setConnections(self, connectionsIN): ## sets connections
        for c in connectionsIN:
            self.connections.append(c)

    def setCircle(self, circleIN): # sets the circle
        self.circle.append(circleIN)

    def  setLine(self, pos, cptIn, size, outlinePX): #sets the end line
        #this gives us (x, y)
        x = pos[0]
        y = pos[1]

        cpt = cptIn.split(", ")
        cptX = float(cpt[0])
        cptY = float(cpt[1])

        slope = (cptY-y)/(cptX-x)

        x6 = 300 ##arbitrary, as we normalize in a short bit
        y6 = (slope)*(x6 - x) + y

        dist = math.sqrt(((x6-x)**2)+((y6-y)**2))
        if (dist==0):
            dist=.001
        normVec =[(x6-x)/dist, (y6-y)/dist]
        newX1 = (normVec[0]*size)+x
        newY1 = (normVec[1]*size)+y

        newX2 = -(normVec[0]*size)+x
        newY2 = -(normVec[1]*size)+y

        newX3 = (normVec[0]*(size+outlinePX))+x
        newY3 = (normVec[1]*(size+outlinePX))+y

        newX4 = -(normVec[0]*(size+outlinePX))+x
        newY4 = -(normVec[1]*(size+outlinePX))+y

        endLine = (newX1, newY1, newX2, newY2)
        endLineOutline = (newX3, newY3, newX4, newY4)
        out = [endLine, endLineOutline]
        self.line.append(out)

    def conToPath(self, globalOffset, distDivide, alt, alternating):
        newString = ""
        for i in range(len(self.connections)): # loop through connections
            current = self.connections[i] #set current connection
            if(i==0): ## if it's the beginning
                newString = f'M{current.aPT()} Q{current.controlPoint(globalOffset, distDivide, alt)}, {current.bPT()} '
            else: ##otherwise just add
                newString = newString + f'{current.controlPoint(globalOffset, distDivide, alt)}, {current.bPT()} '
            if(alternating):
                alt = alt * -1
        self.pathString = newString
        self.pathed = True
        return alt


    def retSymbol(self):
        return aggdraw.Symbol(self.pathString)
