# -*- coding: utf-8 -*-

import logging
import discord
from discord.ext import commands

log = logging.getLogger(__name__)

class News:
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass
