# -*- coding: UTF-8 -*-

import logging
import discord
from discord.ext import commands
import random

log = logging.getLogger(__name__)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        log.info('add call')
        await ctx.send(left + right)

