## dispLayout.py


import os
import shelve
from PIL import Image, ImageDraw, ImageFont
from conf import *

layoutName = "geomabet"
layout = {}
fontSize = 50


back = Image.open(sigilImagesPath+"blank.png")
set="abcdefghijklmnopqrstuvwxyz".upper()
draw = ImageDraw.Draw(back)



with shelve.open(layoutsPath, writeback=False) as f:
        layout = f[layoutName]
        print(layout)

myFont = ImageFont.truetype(os.path.dirname(__file__)+"\\fonts\\aloeVera.ttf", size=fontSize)

for i in range(len(set)):
    pos = layout[set[i]]
    draw.text(pos, set[i], fill=(255, 0, 0), anchor="mm", font=myFont)

back.show()
