import logging
import discord
from discord.ext import commands
import random

log = logging.getLogger(__name__)

class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # defino un group command
    @commands.group()
    async def faq(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    # defino un subcommand
    @faq.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @faq.command()
    async def test(self, ctx, *args):
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))