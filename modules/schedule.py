# -*- coding: utf-8 -*-

import os
import logging
import discord
from discord.ext import commands

import apscheduler
import datetime

from libs.database import Database as DB

log = logging.getLogger(__name__)

class Schedule(commands.Cog):
    """
    Módulo Schedule

    Programa un evento y da aviso con las siguientes frecuencias:
    - 1 día antes
    - 1 hora antes
    - 10 minutos antes

    Comandos:
        !schedule add <url> <date> <time> <time_zone>
        !schedule list
        !schedule remove <id>
        !schedule help

    Ejemplo:
        !schedule add https://google.com 2020-11-26 19:00:00 -03:00
        !schedule remove 12345
    """
    def __init__(self, bot):
        secret = os.getenv("FAUNADB_SECRET_KEY")
        print(f"Secret: {secret}")
        self.bot = bot
        self.db = DB(secret)

    @commands.Cog.listener()
    async def on_ready(self):
        # inicializo el schedule para que corra en backgroud
        log.info("Wait events")

    @commands.group()
    async def schedule(self, ctx):
        pass

    @schedule.command()
    async def add(self, ctx, url, date, time, time_zone):
        try:
            iso_datetime = datetime.datetime.fromisoformat(f"{date}T{time}{time_zone}")

        except ValueError:
            await ctx.send(f"Formato de fecha incorecto: {ValueError}")

        log.info("schedule add")
        pass

    @schedule.command()
    async def list(self, ctx):
        self.db.get_all("all_events")
        return

    @schedule.command()
    async def remove(self, ctx):
        pass

    @schedule.command()
    async def help(self, ctx):
        PREFIX = os.getenv("DISCORD_PREFIX")
        msg = "```go\n`Comando " + PREFIX + "schedule`\n```\n" + \
        "**`" + PREFIX + "schedule add`**     ->  programa un nuevo evento.\n" + \
        "**`" + PREFIX + "schedule list`**    ->  lista los eventos pendientes.\n" + \
        "**`" + PREFIX + "schedule remove`**  ->  elimina un evento programado.\n"
        await ctx.send(msg)

class Delta:
    day = None
    hour = None
    ten_min = None

class EventSched:
    def __init__(self):
        self.delta = Delta()
        self.delta.day = datetime.timedelta(days=-1)
        self.delta.hour = datetime.timedelta(hours=-1)
        self.delta.ten_min = datetime.timedelta(minutes=-10)

        FAUNADB_SECRET_KEY = os.getenv("FAUNADB_SECRET_KEY")
        if FAUNADB_SECRET_KEY == None:
            log.info("FAUNADB_SECRET_KEY don't found")
            return

    def add(self, url, date, time, time_zone):
        try:
            iso_datetime = datetime.datetime.fromisoformat(f"{date}T{time}{time_zone}")

        except ValueError:
            return(f"Formato de fecha incorecto: {ValueError}")

    def start(self):
        pass
