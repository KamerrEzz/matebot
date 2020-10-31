# Modulo faq.py
# FrontEndCafe

#///---- Imports ----///
import logging
import discord
from discord.ext import commands
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

#///---- Log ----///
log = logging.getLogger(__name__)

#///---- Clase ----///
class FAQ(commands.Cog):
    def __init__(self, bot):
        '''
        __init__ del bot (importa este codigo como modulo al bot)
        '''
        self.bot = bot
    
    #! Comando faq
    @commands.group()
    async def faq(self, ctx):
        '''
        Comando !faq
        '''
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    #! Subcomando ping
    @faq.command()
    async def ping(self, ctx):
        '''
        Descripcion: Comando Ping Pong
        Precondicion: Escribir en un canal '!faq ping'
        Poscondicion: Devuelve 'pong'
        '''
        await ctx.send('pong')

    #! Subcomando test
    @faq.command()
    async def test(self, ctx, *args):
        '''
        Descripcion: Comando Test
        Precondicion: Escribir en un canal '!faq test arg1 arg2 ... argN'
        Poscondicion: Devuelve numero de argumentos y cuales son
        '''
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))