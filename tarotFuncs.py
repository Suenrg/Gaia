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

class Card (menus.Menu): #create the card class, for storing tarot card objects
    def __init__(self, name, icon, upright, reverse, upLong, revLong):
        self.name = name
        self.icon = icon
        self.upright = upright
        self.reverse = reverse
        self.upLong = upLong
        self.revLong = revLong
    def prints(self):
        print(f"Name: {self.name}, Up: {self.up}, Rev: {self.rev}, upLong: {self.upLong}, revLong: {self.revLong}")


async def drawCard(mess, deck, art, prompt, ctx):
    seed = prompt + str(datetime.now())
    random.seed(seed)
    choice = random.choice(list(deck.items()))
    card = choice[1]
    print(f"Choice: {choice}")
    await dispCard(mess, card, art, ctx)
    return [card, art]
    # choice = random.choice(list(meanings.items()))


async def dispCard(mess, card, art, ctx):
    print(f'displaying card: {card.name}')
    cardIcon = imgPath + art + "\\" + card.icon
    msg = nextcord.Embed(title=card.name, description=(card.upright), color=mess.author.color)
    file = nextcord.File(cardIcon, filename="image.png")
    msg.set_image(url=f"attachment://image.png")

    sentMess = await mess.channel.send(file=file, embed=msg)
    await moreButton(sentMess, card).start(ctx)
    

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

class moreButton(menus.Menu):
    def __init__(self, message, card):
        super().__init__(timeout=1000, message=message)
        self.mess = message
        self.card = card
        print(f"\n\n menu :  {self}")

    @menus.button('❓')
    async def detail(self, payload):
        print (f"made it here!")
        await self.mess.channel.send(content=f'Thanks {self}!')
        
        

        # self.add_button(button, react=True)

        
    

    
   
        