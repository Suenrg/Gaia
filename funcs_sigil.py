##funcs_sigil.py bea shakow 2022

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

def circlePoints(pos, radius):
    topLeftX = pos[0] - radius ## and then the coords for the circle
    topLeftY = pos[1] - radius
    botRightX = pos[0] + radius
    botRightY = pos[1] + radius
    ret = [topLeftX, topLeftY, botRightX, botRightY]
    return ret
