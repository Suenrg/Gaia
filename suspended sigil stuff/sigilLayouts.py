##sigilLayouts.py Bea Shakow 2022

import os
import shelve
import numpy as np

from PIL import Image, ImageDraw, ImageFont

path = os.path.dirname(__file__)+"\\images\\"

back = Image.open(path+"blank.png")

draw = ImageDraw.Draw(back)

## set up the set into a list
set="abcdefghijklmnopqrstuvwxyz0123456789".upper()
list = []
for i in set:
    list.append(i)

print(len(list))

filePath="layouts.txt"
fontSize = 100
canX = 600
canY = 600
leng = fontSize
startX = leng/2
startY = leng/2+10
lineWidth = 10
layout={}





myFont = ImageFont.truetype(os.path.dirname(__file__)+"\\fonts\\aloeVera.ttf", size=fontSize)
#
# pos = np.array([startX, startY])
# xD = [1,1,-1,-2,-1,1,1,2,1,1,-1,-2,-2,-2,-1,1,1,1,2,2,.5,1.5,1,-1,-1,-1,-1,-1]
# yD = [-1,1,1,0,-1,-1,-1,0,1,1,1,1,0,-1,-1,-1,-1,-1,0,0,1,1,1,1,1,1,1]
# cap = 1
# count = 0
# h=leng/2
# flip = 0
#
#
# for i in range(len(list)):
#     draw.text(pos, list[i], fill=(255, 0, 0), anchor="mm", font=myFont)
#     layout[list[i]] = (int(pos[0]), int(pos[1]))
#     pos = pos + [h*xD[i], leng*yD[i]]
    # count+=1
    # if (count==cap):
    #
    #     yD *= -1
    #     cap += 1
    #     count = 0
    #     flip += 1
    #     if (flip==2):
    #         yD = 0
    #         xD = -2
    #         flip=0


    # if(i==0):
    #     pos = pos + [leng/2, -leng]
    # elif(i==1):
    #     pos = pos + [leng/2, leng]
    # elif(i==2):
    #     pos = pos + [-leng/2, leng]
    # elif(i==3):
    #     pos = pos + [-leng, 0]
    # elif(i==4):
    #     pos = pos + [-leng/2, -leng]
    # elif(i==5):
    #     pos = pos + [leng/2, -leng]
    # elif(i==6):
    #     pos = pos + [leng/2, -leng]
    # elif(i==7):
    #     pos = pos + [leng, 0]
    # elif(i==8):
    #     pos = pos + [leng/2, leng]


count = 0
for y in range(int(canY/leng)):
    for x in range(int(canX/leng)):
        if (count >= len(set)):
            break
        pos = (int(x*leng+startX), int(y*leng+startY))
        draw.text(pos, list[count], fill=(255, 0, 0), anchor="mm", font=myFont)
        layout[list[count]] = pos
        count +=1

#
# def connect(one, two):
#     draw.line([layout[one], layout[two]], fill=("#4324AD"), width=lineWidth)
#
# connect('n', 'e')
# connect('e', 'w')
#
# connect('g','a')
# connect('a','i')
# connect('i','a')

# with shelve.open(filePath, writeback=True) as f:
    #f["rect"]=layout





print(layout)
back.show()
# back.save(path+"rectLayout.png")
