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
from datetime import datetime
from gaiaSigils import *

load_dotenv() #token stuff
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#### variables
test_guild_id = 775449492232208404
guilds=[727652231419002880, 775449492232208404, 572854786513174529, 923448242107207720]
prefix="!g"
intents = nextcord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
##### filepaths
vaultPath = os.path.dirname(__file__)+"\\vault\\"


####

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:\n')
    for guild in bot.guilds:
        # await client.change_presence(status=discord.Status.online, activity=discord.Game("!t help"))
        print(f'{guild.name}(id: {guild.id})') #test guild ID: 775449492232208404


@bot.slash_command(description="Creates a sigil from your phrase!", guild_ids=guilds)
async def sigil(
    ctx,
    phrase: str,
    flip: bool=False,
    nonalternating: bool = SlashOption(name="nonalternating", required=False, default=False),
    layout: str = SlashOption(name="layout", choices=["spiral", "rect"], required=False, default="spiral"),
    randcolor: bool = SlashOption(name="random_color", required=False, default=True),
    colors: str = SlashOption(name="colors", required=False, default="#4324AD"),
    lines: bool = SlashOption(name="lines", required=False, default=False)
    ):
    print(f"##################\nRunning sigil with phrase {phrase}")
    sigilFile = await sigils(ctx, phrase, flip, nonalternating, layout, randcolor, colors, lines)
    file = nextcord.File(sigilFile, filename="image.png")
    sigilEmbed = nextcord.Embed()
    sigilEmbed.title = phrase.upper()
    sigilEmbed.set_image(url=f"attachment://image.png")
    await ctx.send(file=file, embed=sigilEmbed)

@bot.slash_command(description="Creates all 4 permutations of a sigil phrase.", guild_ids=guilds)
async def allsigils(
    ctx,
    phrase: str,
    layout: str = SlashOption(name="layout", choices=["spiral", "rect"], required=False, default="spiral"),
    lines: bool = SlashOption(name="lines", required=False, default=False)
    ):
    flip = False
    nonAlt = False
    params = [flip,nonAlt]
    numparams = len(params)
    count = 0
    for p in range(numparams**2):
        sigilFile = await sigils(ctx, phrase, params[0], params[1],layout,True,"#4324AD",lines)
        file = nextcord.File(sigilFile, filename="image.png")
        sigilEmbed = nextcord.Embed()
        sigilEmbed.title = phrase.upper()
        sigilEmbed.description = f"Flip = {params[0]}, nonalternating = {params[1]}"
        sigilEmbed.set_image(url=f"attachment://image.png")
        await ctx.send(file=file, embed=sigilEmbed)
        params[0] = not params[0]
        if (p%numparams == numparams - 1):
            params[1] = not params[1]




### Runs the bot!!
bot.run(TOKEN)
