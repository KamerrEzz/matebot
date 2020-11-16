# -*- coding: utf-8 -*-

import os
import logging
from datetime import timedelta

import discord
from discord.ext import commands

from libs.database import Database as DB
from libs.reminder import Reminder

log = logging.getLogger(__name__)

class Scheduler(commands.Cog):
    """
    Módulo Scheduler

    Programa un evento y da aviso con las siguientes frecuencias:
    - 1 día antes
    - 1 hora antes
    - 10 minutos antes

    Comandos:
        !sched add <url> <date> <time> <time_zone> <channel>
        !sched list
        !sched remove <id>
        !sched help

    Ejemplo:
        !sched add https://google.com 2020-11-26 19:00:00 -03:00 #eventos
        !sched remove 12345
    """
    def __init__(self, bot):
        self.bot = bot
        secret = os.getenv("FAUNADB_SECRET_KEY")
        self.reminder = Reminder(secret)

        # Defino la función que se utiliza para ejecutar los eventos
        self.reminder.action = self.action
        # Defino los recodatorios
        self.reminder.reminders = [
            {"delta": timedelta(days=1),     "message": "Mañana comenzamos, te esperamos!!"},
            {"delta": timedelta(hours=1),    "message": "Nos estamos preparando, en 1 hora arrancamos!!"},
            {"delta": timedelta(minutes=10), "message": "En 10 minutos arrancamos, no te lo pierdas!!"}
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Load events from database")
        await self.reminder.load()

    @commands.group()
    async def sched(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Commando inválido ...')

    @sched.command()
    async def add(self, ctx, url, date, time, time_zone, channel_id):
        log.info("Add new event to scheduler")
        try:
            doc = await self.reminder.add(ctx.author, url, date, time, time_zone, channel_id)
            if doc == []:
                await ctx.send("ERROR: especifique una fecha posterior a la fecha actual.")
                return
            msg = self.generate_msg(doc, "Evento agregado")
            await ctx.send(msg)
        except:
            log.info("Error: datetime format error")
            await ctx.send("ERROR: por favor verifique el formato introducido.")

    @sched.command()
    async def list(self, ctx):
        docs = await self.reminder.list()
        msg_in = ""
        msg = ""
        if docs != []:
            for doc in docs:
                msg_in = msg_in + "- {0} | {1} | {2}\n".format(
                    doc['ref'].id(),
                    doc['data']['time'].value,
                    doc['data']['author']
                )
            msg = "```md\n### Lista de eventos ###\n\n- id | time | author\n{}```".format(msg_in)
        else:
            msg = "```md\n### Lista vacía ###\n```"
        await ctx.send(msg)

    @sched.command()
    async def remove(self, ctx, id_: str):
        log.info(ctx.author)
        doc = await self.reminder.remove(id_)
        msg = self.generate_msg(doc, "Evento eliminado")
        await ctx.send(msg)

    @sched.command()
    async def help(self, ctx):
        PREFIX = os.getenv("DISCORD_PREFIX")
        msg = f"""
```md
### COMANDO {PREFIX}sched ###

- {PREFIX}sched add: Programa un nuevo evento.
- {PREFIX}sched list: Lista los eventos pendientes.
- {PREFIX}sched remove: Elimina un evento programado.
- {PREFIX}sched help: Muestra la ayuda.

Ejemplos:
    {PREFIX}sched add <url> <date> <time> <time_zone> <channel>
    {PREFIX}sched add https://google.com 2019-12-24 22:00:00 -03:00 #my-channel

    {PREFIX}sched list

    {PREFIX}sched remove <id>
    {PREFIX}sched remove 281547393529283072
```
        """
        await ctx.send(msg)

    def generate_msg(self, doc, title):
        return "```md\n# {}\n".format(title) + \
            "- id:     {}\n"    .format(doc['ref'].id()) + \
            "- time:   {} UTC\n".format(doc['data']['time'].value) + \
            "- author: {}\n```" .format(doc['data']['author'])

    async def action(self, msg, url, channel_id):
        channel = self.bot.get_channel(channel_id)
        await channel.send(f"{msg}\n\n{url}")
