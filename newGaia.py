# newGaia.py
import os
import sys
import random
import asyncio
import shelve
from dotenv import load_dotenv
import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
from nextcord.ext import menus
from datetime import datetime
# from gaiaSigils import *
from cardDecks import *
from tarotFuncs import *
from conf import *

load_dotenv() #token stuff
TOKEN = os.getenv('DISCORD_TOKEN')
# print(TOKEN)
GUILD = os.getenv('DISCORD_GUILD')

#### variables
test_guild_id = 572854786513174529
guilds=[]#727652231419002880, 775449492232208404, 572854786513174529, 923448242107207720, 1149038131673309324]
prefix="!g"
intents = nextcord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
callAt = "<@1024094680968855663>"
talkChance = 100 ##higher is less probable
##### filepaths


####

bot = commands.Bot(command_prefix=prefix, intents=intents)


#### Load decks and deckPrefs
decks = loadDecks(meaningsPath)

####

@bot.event #start gaia up, show what guilds we're connected to 
async def on_ready():
    guilds=bot.guilds
    print(f'{bot.user} is connected to the following guilds:\n')
    for guild in guilds:
        await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game("! try /gaiatalking also !t help"))
        print(f'{guild.name}(id: {guild.id})') #test guild ID: 775449492232208404
       

## Tarot stuff
##|||||||||||
##vvvvvvvvvvv

## slash command card
# @bot.slash_command(description="Draws a tarot card!", guild_ids=guilds)
# async def drawcard(
#     ctx,
#     prompt: str = SlashOption(name='prompt', required=False, default=""),
#     ):
#     ## load deckPrefs
#     messageAuthor = str(ctx.user)
#     prefs = await getPrefs(deckPrefsPath, messageAuthor)
#     print(f"##################\nRunning tarot with deck: {prefs[0]} and art {prefs[1]} prefs: {type(prefs)}")
#     sendDeck = decks[prefs[0]]
#     sendArt = prefs[1]
#     print(ctx)
#     await drawCard(ctx.message, sendDeck, sendArt, prompt)

## on_message controls
@bot.event
async def on_message(message):
    if message.author == bot.user: #don't talk to urself
        return
    ctx = await bot.get_context(message)
    if(message.content.startswith(prefix) or callAt in message.content): ##are we in a command? checking for prefix or callAt
        print(f"##################\nCommand Recieved:\n\"{message.content}\"\n{message} ")
        messageAuthor = str(message.author.name) #message author
        prefs = await getPrefs(deckPrefsPath, messageAuthor)
        sendDeck = decks[prefs[0]]
        sendArt = prefs[1]

        check = await checkMessage(message, sendDeck)
        
        if (check == None):
            await drawCard(message, sendDeck, sendArt, message.content, ctx)
        else:
            await dispCard(message, check, sendArt, ctx)

    
    ##### handle  talking chances
    elif not(str(message.author.id) in callAt):
        # print(f"{message.author.id}")
        cID = str(message.channel.id) ##message channel id
        guildID = str(message.channel.guild.id) # what guild are we in?
        everywhere = False
        with shelve.open(talkingChannelsPath, writeback=True) as s: #open talkingChannels shelf
            if (guildID in s): #if this guild is in there
                if('everywhere' in s[guildID]):
                    everywhere = s[guildID]['everywhere']
                if (cID in s[guildID]) or everywhere: #if this channel is in there or everywhere is on

                    if(not cID in s[guildID]):
                        s[guildID][cID] = {}
                        s[guildID][cID]['talks'] = False
                        s[guildID][cID]['chance'] = talkChance
                        s[guildID][cID]['count'] = 0

                    if(everywhere or s[guildID][cID]['talks'] == True):  #if talking is allowed
                        current = s[guildID][cID]
                        chance = random.randint(0,current['chance']) #random chance
                        if(chance > current['count']):
                            current['count'] += 1
                            print(f"not talking, count is {current['count']}, had to be bigger than {chance}")
                        elif(chance <= current['count']):
                            print(f"talking! count is {current['count']}, was bigger than {chance}")
                            with open("talkingChanceData.csv", "a") as myfile:
                                myfile.write(f"{current['count']},")
                            current['count'] = 0
                            prefArt = random.choice(artChoices)
                            prefDeck = decks['Biddy']
                            s.close()
                            await drawCard(message, prefDeck, prefArt, message.content, ctx)
                        print(f"Chance: {str(chance)} Count: {str(current['count'])} \n")

# # Drawing cards
# @bot.command()
# async def drawCommand(ctx, mess, deck, art, prompt):
#     print(ctx)
#     await drawCard(mess, deck, art, prompt, ctx)

## deck prefences
@bot.slash_command(description="Sets which deck you want Gaia to use for you!", guild_ids=guilds)
async def choosedeck(
    ctx,
    deck: str = SlashOption(name="deck", choices=deckChoices, required=False, default=defaultDeck),
    art: str = SlashOption(name="art", choices=artChoices, required=True, default=defaultArt)
    ):
    messageAuthor = str(ctx.user.name)
    print(f"##################\nSaving prefs for {messageAuthor} with deck {deck}")
    await savePrefs(deckPrefsPath, messageAuthor, deck, art)
    await ctx.send(f'Saved your preferences with art: {art} and deck: {deck}')

@bot.slash_command(description="Lets Gaia talk in this channel freely (has a small chance to respond to a message with a card)", guild_ids=guilds)
async def gaiatalking(
    ctx,
    talks: bool = SlashOption(name="talks", required=False, default=True),
    everywhere: bool = SlashOption(name="everywhere", required=False, default=False)
    ):
    messageAuthor = str(ctx.user.name)
    cID = str(ctx.channel.id)
    guildID = str(ctx.channel.guild.id)
    print(f"##################\nLetting Gaia talk in channel:{cID} in guild:{guildID} for {messageAuthor} ")
    with shelve.open(talkingChannelsPath, writeback=True) as s:
        if not(guildID in s):
            s[guildID] = {}
            s[guildID]['everywhere'] = False
        s[guildID]['everywhere'] = everywhere
        s[guildID][cID] = {}
        s[guildID][cID]['talks'] = talks
        s[guildID][cID]['chance'] = talkChance
        s[guildID][cID]['count'] = 0
        print(f"s[guildID][cID] = {s[guildID][cID]}")
    await ctx.send(f"Gaia can talk in this channel: {talks}")



# ## Sigil stuff
# ## ||||||||||
# ## vvvvvvvvv


# @bot.slash_command(description="Creates a sigil from your phrase!", guild_ids=guilds)
# async def sigil(
#     ctx,
#     phrase: str,
#     flip: bool=False,
#     nonalternating: bool = SlashOption(name="nonalternating", required=False, default=False),
#     layout: str = SlashOption(name="layout", choices=layoutChoices, required=False, default="spiral"),
#     randcolor: bool = SlashOption(name="random_color", required=False, default=True),
#     colors: str = SlashOption(name="colors", required=False, default="#4324AD"),
#     lines: bool = SlashOption(name="lines", required=False, default=False)
#     ):
#     print(f"##################\nRunning sigil with phrase {phrase}")
#     sigilFile = await sigils(ctx, phrase, flip, nonalternating, layout, randcolor, colors, lines)
#     file = nextcord.File(sigilFile, filename="image.png")
#     sigilEmbed = nextcord.Embed()
#     sigilEmbed.title = phrase.upper()
#     sigilEmbed.set_image(url=f"attachment://image.png")
#     await ctx.send(file=file, embed=sigilEmbed)

# @bot.slash_command(description="Creates all 4 permutations of a sigil phrase.", guild_ids=guilds)
# async def allsigils(
#     ctx,
#     phrase: str,
#     layout: str = SlashOption(name="layout", choices=layoutChoices, required=False, default="spiral"),
#     lines: bool = SlashOption(name="lines", required=False, default=False)
#     ):
#     flip = False
#     nonAlt = False
#     params = [flip,nonAlt]
#     numparams = len(params)
#     count = 0
#     for p in range(numparams**2):
#         sigilFile = await sigils(ctx, phrase, params[0], params[1],layout,True,"#4324AD",lines)
#         file = nextcord.File(sigilFile, filename="image.png")
#         sigilEmbed = nextcord.Embed()
#         sigilEmbed.title = phrase.upper()
#         sigilEmbed.description = f"Flip = {params[0]}, nonalternating = {params[1]}"
#         sigilEmbed.set_image(url=f"attachment://image.png")
#         await ctx.send(file=file, embed=sigilEmbed)
#         params[0] = not params[0]
#         if (p%numparams == numparams - 1):
#             params[1] = not params[1]

# ###




### Runs the bot!!
bot.run(TOKEN)
