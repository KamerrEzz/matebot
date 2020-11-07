# Modulo faq.py
# FrontEndCafe

#///---- Imports ----///
import logging
import discord
from discord.ext import commands
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import re
from dotenv import load_dotenv
import os

#///---- Log ----///
log = logging.getLogger(__name__)

#///---- Clase ----///
class FAQ(commands.Cog):
    '''
    Consulta y edición de FAQ:
    Los comandos son los siguientes:
        - !faq help --> Lista de subcomandos disponibles en FAQ.
        - !faq all --> Envía por DM al usuario todo el FAQ completo.
        - !faq 
    '''
    def __init__(self, bot):
        '''
        __init__ del bot (importa este codigo como modulo al bot)
        '''
        self.bot = bot
    #! !faq
    #! Comando faq
    @commands.group()
    async def faq(self, ctx):
        '''
        Comando !faq
        '''
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    #! Subcomando help
    @faq.command()
    async def help(self, ctx):
        '''
        Descripción: Ayuda de FAQ
        Precondicion: Escribir en un canal !faq help
        Poscondición: El bot escribe lista de comandos con descripción
        '''
        lines = '''
```
!faq help: Ayuda del FAQ
!faq all: Por DM recibís el FAQ completo
!faq projects: Breve explicación de los proyectos en FEC, mostrando cuales están activos
!faq roles: Breve explicación de cada rol
```
                '''
        await ctx.send(lines)
        

    #! Subcomando all
    @faq.command()
    async def all(self, ctx):
        '''
        Descripción: FAQ completo por DM
        Precondición: Escribir en un canal !faq all
        Poscondición: El bot envía por DM el FAQ
        '''
        load_dotenv()
        DB_KEY = os.getenv("FAUNADB_SECKEY")
        client = FaunaClient(secret = DB_KEY)
        dato = ''

        # Indezacion de datos
        allfaqs = client.query(
            q.paginate(
                q.match(q.index('allfaqs'))
            )
        )
        allfaqslist = [allfaqs['data']]
        # print(allfaqslist) # Muestra los Ref de cada dato en 'data'
        result = re.findall('\d+', str(allfaqslist))
        # print(result) # Muestra los resultados de allfaqslist en strings (una cosa fea)

        for i in range(0, len(result), 1):
            # print(result[i]) # Muestra los Ref de cada dato
            faqdetails = client.query(q.get(q.ref(q.collection('faqs'), result[i])))
            detailslist = [faqdetails['data']]
            # print(detailslist) # Muestro lista de diccionario con datos
            dato += f'Nombre de usuario: {detailslist[0].get("UserName")} \tContrasenia: {detailslist[0].get("Password")}\n'
        await ctx.author.send(dato)


    # #! Subcomando ping
    # @faq.command()
    # async def ping(self, ctx):
    #     '''
    #     Descripcion: Comando Ping Pong
    #     Precondicion: Escribir en un canal '!faq ping'
    #     Poscondicion: Devuelve 'pong'
    #     '''
    #     await ctx.send('pong')

    # #! Subcomando test
    # @faq.command()
    # async def test(self, ctx, *args):
    #     '''
    #     Descripcion: Comando Test
    #     Precondicion: Escribir en un canal '!faq test arg1 arg2 ... argN'
    #     Poscondicion: Devuelve numero de argumentos y cuales son
    #     '''
    #     await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))