## async_connection.py bea Shakow 2022

import numpy as np

class connection:
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

    def controlPoint(self, offset, alt):
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
        final_vec = unit_vec*offset
        #print(final_vec)
        nX = int(x3 + final_vec[0])
        nY = int(y3 + final_vec[1])
        #print(f'nX: {nX},   nY: {nY}')
        return f'{nX}, {nY}'

    def prints(self):
        print(f'a = {self.a}: {self.layout[self.a]} ; b = {self.b}: {self.layout[self.b]}')
