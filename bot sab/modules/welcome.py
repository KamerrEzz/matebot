# Modulo welcome.py

import logging
import discord
from discord.ext import commands
import re
from dotenv import load_dotenv
import os
import asyncio

intents=discord.Intents.default()
intents.members=True


class WELCOME(commands.Cog):
    '''
    Saludo de bienvenida al server
    '''
    def __init__(self, bot):
        '''
        __init__ del bot (importa este codigo como modulo al bot)
        '''
        self.bot = bot
    
    #! Comando 
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Hola! Que bueno verte por acá.\nTe cuento, FrontendCafé es una comunidad de personas interesadas en tecnología y ciencias informáticas en donde charlamos sobre lenguajes de programación, diseño web, infraestructura, compartimos dudas, preguntamos y respondemos. Compartimos recursos, artículos, cursos, e información sobre eventos, nos auto-organizamos en grupos para estudiar, hacer proyectos juntos, y charlar en inglés para perfeccionarnos. \nTambién nos vamos de after office, y jugamos jueguitos.\nAcá dejo el Código de conducta #📜︱codigo-de-conducta!\nY acá el manual de uso #📜︱manual-de-us')