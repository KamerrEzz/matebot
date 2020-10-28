# proyecto matebot en frontendcafe

## La estructura que he realizado

*   [+] [kamerr.py](#Kamerr) Archivo principal
*   [+] [cogs](#COGS) | comandos
    *   [-] `FAQ` los comandos que tiene relacion con FAQ
    *   [-] `Greeting` un evento de bienvenida y el comando de saludar

<a name="Kamerr"></a>

## Archivo Principal

En este archivo lo que hace son inicamente las peticiones y usando la extension [discord.ext](https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html) para simplicar muchas cosas.

aun que no logro saber si puedo cambiar algunas opciones de respuesta automaticas, o hacerlas desde cero.

> la estructura es mucho mas limpia y ordenada

<a name="COGS"></a>

## Estructura COGs

Por lo que entendido seria un command handler o una forma de estructurar y ordenar los comandos por clases y tener una mejor estructura

esta informacion se encuentra en la [documentacion](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html#)

### Estructura

```python
import discord # el modulo
from discord.ext import commands # La extencion

# La clase donde se menteran los comandos, como categoria
class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    ## este es un evento que se activa cuando un usuario ingresa al servidor
    ## Puede ser opcional
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    # Obviamente el comando
    @commands.command()
    async def hello(self, ctx,):
        await ctx.send("Hola")


# A qui le decimos que lo cargue
def setup(client):
    client.add_cog(Greetings(client))
```