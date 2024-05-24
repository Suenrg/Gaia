##gaiaTarot.py bea shakow 2022
import os
import sys
import random
import asyncio
import shelve
import sqlite3
from datetime import datetime
from conf import *
import nextcord
from nextcord.ext import menus
from buttonClasses import *

#Setup database
def setupDatabase():
      with sqlite3.connect(database) as conn:
        cur = conn.cursor()
        setupTable = """
        CREATE TABLE IF NOT EXISTS Users (
        Name      TEXT,
        userID    INTEGER,
        daily     TEXT,
        dailyDate INTEGER,
        art       TEXT,
        meanings  TEXT
        );"""
        print(cur.execute(setupTable)) #name, userID, daily, dailyDate, art, meanings
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

async def drawCard(mess, deck, art, prompt, ctx, disp):
    seed = prompt + str(datetime.now())
    random.seed(seed)
    choice = random.choice(list(deck.items()))
    card = choice[1]
    print(f"Choice: {card}")
    if disp:
        await dispCard(mess, card, art, ctx)
    return [card, art]
    # choice = random.choice(list(meanings.items()))


# {message, card, art, ctx} -> DISPLAY -> {msg{embed}} {fullButton} 

async def dispCard(mess, card, art, ctx):
    print(f'displaying card: {card.name}, with art {art}')
    cardIcon = imgPath + art + "\\" + card.icon
    msg = nextcord.Embed(title=card.name, description=(card.upright), color=mess.author.color)
    file = nextcord.File(cardIcon, filename="image.png")
    msg.set_image(url=f"attachment://image.png")
    button = await fullButton(ctx,file,msg.copy(),card).go(ctx)
    
async def checkCardAsk(mess, deck): #check to see if they're asking about a card
    for i in deck:
        if (i.lower() in mess.content.lower()): 
            print(f"Check returning {deck[i]}")
            return deck[i]
    return None

async def checkCommandAsk(mess): #checks to see if there's a command
    if "daily" in mess.content.lower():
        return "daily"
    else:
        return None



##DAILY PULL

async def dailyPull(mess, deck, art, ctx):
    user = str(mess.author)
    id = str(mess.author.id)
    dailyDate = datetime.now().day
   # print(f"user = {user}, id = {id}, date = {dailyDate}")
    try:
        with sqlite3.connect(database) as conn: # connect to the database
            cur = conn.cursor()
            query = cur.execute("""
            SELECT name, userid, daily, dailyDate FROM Users WHERE userID = ?
            """, (id,)).fetchone() ##check to see if we have them in the database
            #if we do, then check their daily date
            if query != None: #if they exist
                print (f'sql column for user: {query}')
                #and we already have their card for today
                if query[3] == dailyDate:
                    print(f'Already pulled a daily for them, {query[2]}')
                    conn.close()
                    #display it to them
                    await ctx.send(f"Already pulled a daily card for you today:")
                    await dispCard(mess, deck[query[2]], art, ctx)
                    return deck[query[2]]
            #if they don't exist, or if they're out of date, draw them a card
            await ctx.send(f"{user}, your Daily card is:")
            card = await drawCard(mess, deck, art, mess.content, ctx, False)
            print(f"card name = {card[0].name}")
            #and add it to our database
            cur.execute("""INSERT INTO Users (name, userID, daily, dailyDate) VALUES(?,?,?,?)""",(user,id,card[0].name,dailyDate,))
            conn.commit()
            conn.close()
            #then display it for them
            await dispCard(mess, card[0], art, ctx)
            
    except sqlite3.Error as error:
        print("Error while connecting to SQLITE3: "+ str(error))


### PREFERENCES

async def savePrefs(deckPrefsPath, name, deck, art):
    with shelve.open(deckPrefsPath, writeback=True) as shelf:
        if not name in shelf:
            shelf[name] = {}
        shelf[name]['deck'] = deck
        shelf[name]['art'] = art
    print(f'Saved prefs for {name}, Deck: {deck}, art: {art}')

async def getPrefs(deckPrefsPath, name):
    deck = ""
    art = ""
    with shelve.open(deckPrefsPath) as s: ##open deckprefs
        if (name in s): ##if they are in the doc and have deck
            print(f'getting prefs for {name}')
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
    print(f'{name} is using prefs {deck}, {art} ')
    return [deck, art]


 
        
    

    
   
        