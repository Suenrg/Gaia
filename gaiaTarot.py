##gaiaTarot.py bea shakow 2022
import os
import sys
import random
import asyncio
import shelve
from datetime import datetime
from conf import *
import nextcord

async def drawCard(mess, deck, art, prompt):
    seed = prompt + str(datetime.now())
    random.seed(seed)
    choice = random.choice(list(deck.items()))
    card = choice[1]
    print(f"Choice: {choice}")
    await dispCard(mess, card, art)
    return [card, art]
    # choice = random.choice(list(meanings.items()))


async def dispCard(mess, card, art):
    print(f'displaying card: {card.name}')
    cardIcon = imgPath + art + "\\" + card.icon
    msg = nextcord.Embed(title=card.name, description=(card.upright), color=mess.author.color)
    file = nextcord.File(cardIcon, filename="image.png")
    msg.set_image(url=f"attachment://image.png")
    await mess.channel.send(file=file, embed=msg)

async def savePrefs(deckPrefsPath, name, deck, art):
    with shelve.open(deckPrefsPath) as s:
        if not name in s:
            s[name] = {}
        s[name]['deck'] = deck
        s[name]['art'] = art

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
