##gaiaTarot.py bea shakow 2023

import os
import sys
import random
import asyncio
import shelve
from datetime import datetime
from conf import *
import nextcord
from nextcord.ext import menus

class fullButton(menus.Menu):
    
    def __init__(self,ctx, file, prepEmbed, card):
        self.prepEmbed = prepEmbed
        self.card = card
        self.file = file
        self.ctx = ctx
        super().__init__(check_embeds=True)
        
 
    async def send_initial_message(self, ctx, channel):
        return await ctx.channel.send(file=self.file, embed=self.prepEmbed)
    
    async def go(self,ctx):
        await self.start(ctx, wait=True)
        # return self.result

    @menus.button('❓')
    async def detail(self, payload):
        # selfText = self.mess
        # print(f'self={selfText}')
        newEmbed = self.prepEmbed.copy()
        newFooter = self.card.fullCard
        newEmbed.set_footer(text=newFooter)
        # print(f'the new embed in full is {newEmbed.footer[:50]}')
        await self.message.edit(embed = newEmbed)
        print('edited at last!')
        
        
    
# class fullPageSource(menus.ListPageSource):
#     def __init__(self, card):
        


#         super().__init__(card.fullCard, per_page=1)

#     async def format_page(self, menu, entries):
#         embed = Embed(title="Entries", description="\n".join(entries))
#         embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
#         return embed
