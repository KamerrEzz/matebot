# -*- coding: UTF-8 -*-

import logging
import discord
from discord.ext import commands
import random

log = logging.getLogger(__name__)

class Music(commands.Cog):
    def __init__(self, bot):
        bot.add_listener(self.on_ready)
        self.bot = bot

    # defino un evento de escucha
    async def on_ready(self):
        print('Logged in as {0} ({0.id})'.format(self.bot.user))
        print('------')

    # los main commands no pueden duplicarse entre clases
    # el objeto bot va registrando todos los comandos con el decorador
    @commands.command()
    async def main_add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        log.info('add call')
        await ctx.send(left + right)

    # defino un command group
    @commands.group()
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    # defino un subcommand
    @music.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        log.info('add call')
        await ctx.send(left + right)

    @music.command()
    async def play(self, ctx, *text):
        log.info('play call')
        await ctx.send(" ".join(text))

