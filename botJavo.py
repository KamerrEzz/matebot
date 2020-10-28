# Bot de javo.py

#! Link de desarrollo: https://discord.com/developers/applications
#! Links de interes:    - https://realpython.com/async-io-python/
#!                      - https://discordpy.readthedocs.io/en/latest/api.html


import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    #!------------ Conexion del bot y aviso
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    '''
    Mensajes automáticos del bot:
        - Con comandos
        - Detectando palabras claves (HACER)
    '''
    prefijo = '!'
    comandos = {
        'saludo': f'Hola! Como andás {message.author.mention}?',
        'invitar': f'Invitá a tus amigos con este enlace: https://discord.gg/Qsa9Nwr',
        'mate': f'Amargo o dulce? :mate:',
        'help': '''
```
!saludo: El bot te saluda
!invitar: Obtenés enlace de invitación al servidor
!mate: El bot te da un matienzo
!help: Obtenés los comandos del bot
```
                '''
    }

    if message.author != client.user: #! Si el autor del mensaje es el bot, no sigo
        if prefijo == message.content[0]: #! Para detectar prefijo
            mensaje = message.content[1:]
            if mensaje in comandos: #! Si el resto del mensaje es un comando del diccionario
                respuesta = comandos[mensaje]
                await message.channel.send(respuesta)


client.run(TOKEN)