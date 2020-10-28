# -*- coding: UTF-8 -*-

import logging
import discord
from discord.ext import commands
import random

log = logging.getLogger(__name__)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def help(self, ctx):
        log.info('Show commands list')

    @help.command()
    async def music(self, ctx):
        log.info("Show subcommand list for `music`")
