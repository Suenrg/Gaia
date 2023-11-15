##gaiaTarot.py bea shakow 2022
import os
import sys
import random
import asyncio
import shelve
from datetime import datetime
from conf import *
import nextcord
from nextcord.ext import menus
from buttonClasses import *

#CARD CLASS

class Card (menus.Menu): #create the card class, for storing tarot card objects
    def __init__(self, name, icon, upright, reverse, fullCard, revLong):
        self.name = name
        self.icon = icon
        self.upright = upright
        self.reverse = reverse
        self.fullCard = fullCard[:1999].rpartition('.')[0] + '.'
        self.revLong = revLong
    def prints(self):
        print(f"Name: {self.name}, Up: {self.up}, Rev: {self.rev}, fullCard: {self.fullCard}, revLong: {self.revLong}")

#  {message, deck, art, prompt, ctx } -> DRAW -> {card, art}

async def drawCard(mess, deck, art, prompt, ctx):
    seed = prompt + str(datetime.now())
    random.seed(seed)
    choice = random.choice(list(deck.items()))
    card = choice[1]
    print(f"Choice: {card}")
    await dispCard(mess, card, art, ctx)
    return [card, art]
    # choice = random.choice(list(meanings.items()))


# {message, card, art, ctx} -> DISPLAY -> {msg{embed}} {fullButton} 

async def dispCard(mess, card, art, ctx):
    print(f'displaying card: {card.name}')
    cardIcon = imgPath + art + "\\" + card.icon
    msg = nextcord.Embed(title=card.name, description=(card.upright), color=mess.author.color)
    file = nextcord.File(cardIcon, filename="image.png")
    msg.set_image(url=f"attachment://image.png")
    button = await fullButton(ctx,file,msg.copy(),card).go(ctx)
    
    

### PREFERENCES

async def savePrefs(deckPrefsPath, name, deck, art):
    with shelve.open(deckPrefsPath) as shelf:
        if not name in shelf:
            shelf[name] = {}
        shelf[name]['deck'] = deck
        shelf[name]['art'] = art

async def getPrefs(deckPrefsPath, name):
    deck = ""
    art = ""
    with shelve.open(deckPrefsPath) as s: ##open deckprefs
        if (name in s): ##if they are in the doc and have deck
            if ('deck' in s[name]): ## if they have a deck
                deck = s[name]['deck'] #choose it
            else:  #otherwise go default
                deck = defaultDeck
            if('art' in s[name]):# if they have an art
                art = s[name]['art']
            else:
                art = defaultArt
        else:
            deck = defaultDeck
            art = defaultArt
    return [deck, art]


 
        
    

    
   
        