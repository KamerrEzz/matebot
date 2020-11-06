# -*- coding: utf-8 -*-

import logging
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

log = logging.getLogger(__name__)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ignoro los comandos que no existen
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, CommandNotFound):
    #         return
    #     raise error
