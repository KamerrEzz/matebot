# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime, timezone, timedelta

import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from libs.database import Database as DB

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
        self.reminder = Reminder(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Load events from database")
        self.reminder.load()

    @commands.group()
    async def sched(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Commando invalido ...')

    @sched.command()
    async def add(self, ctx, url, date, time, time_zone, channel_id):
        log.info("schedule add")
        try:
            date_time = datetime.fromisoformat(f"{date}T{time}{time_zone}")
            date_time_now = datetime.utcnow().replace(tzinfo=timezone.utc)

            if date_time > date_time_now:
                doc = self.reminder.add(ctx.author, url, date_time, channel_id)
                msg = self.generate_msg(doc, "Evento agregado")
                await ctx.send(msg)
            else:
                await ctx.send("ERROR: especifique una fecha posterior a la fecha actual.")
        except:
            log.info("Error: datetime format error")
            await ctx.send("ERROR: por favor verifique el formato introducido.")

    @sched.command()
    async def list(self, ctx):
        docs = self.reminder.list()
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
        doc = self.reminder.remove_by_id(id_)
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

# Manejo los recordatorios
class Reminder:
    def __init__(self, bot):
        # Necesito el objeto bot para poder enviar mensajes
        self.bot = bot

        # Accedo a la base de datos
        secret = os.getenv("FAUNADB_SECRET_KEY")
        self.db = DB(secret)

        # Arranco en Async Scheduler
        self.sched = AsyncIOScheduler()
        self.sched.start()

    def load(self):
        docs = self.db.get_all("all_events")
        new_docs = []
        for doc in docs['data']:
            url = doc['data']['url']
            date_time = datetime.fromisoformat(f"{doc['data']['time'].value[:-1]}+00:00")
            channel_id = doc['data']['channel']

            # Creo los jobs
            jobs_id = self.program_frecuency(url, date_time, channel_id)
            new_docs.append((doc['ref'].id(), {"jobs": jobs_id}))

        # Actulizo la base de datos con los nuevos jobs_id
        self.db.update_all_jobs("Events", new_docs)

    def add(self, author, url, date_time, channel_id):
        author = f"{author}"
        channel_id = int(channel_id[2:][:-1])
        jobs_id = self.program_frecuency(url, date_time, channel_id)

        # Guardo el evento en la base de datos
        data = {
            "author": author,
            "url": url,
            "time": self.db.q.time(date_time.isoformat()),
            "channel": channel_id,
            "jobs": jobs_id
        }

        # Genero un registro local
        return self.db.create("Events", data)

    def list(self):
        events = self.db.get_all("all_events")
        return events['data']

    def program_frecuency(self, url, date_time, channel_id: int):
        dt_event = date_time
        dt_now = datetime.utcnow().replace(tzinfo=timezone.utc)

        # Defino los recodatorios con los mensajes y el tiempo
        reminders = [
            {
                "message": "Mañana comenzamos, te esperamos!!",
                "delta": timedelta(days=1),
                "time": "1 day"
            },
            {
                "message": "Nos estamos preparando, en 1 hora arrancamos!!",
                "delta": timedelta(hours=1),
                "time": "1 hour"
            },
            {
                "message": "En 10 minutos arrancamos, no te lo pierdas!!",
                "delta": timedelta(minutes=10),
                "time": "10 min"
            }
        ]

        jobs_id = []
        for reminder in reminders:
            if dt_event > dt_now + reminder['delta']:
                log.info("Add event %s", reminder['time'])
                job = self.sched.add_job(
                    self.event,
                    'date',
                    run_date=(dt_event - reminder['delta']),
                    args=[reminder['message'], url, channel_id]
                )
                jobs_id.append(job.id)

        # Job para eliminar el registro de la base de datos
        job = self.sched.add_job(
            self.remove_from_db,
            'date',
            run_date=(dt_event + timedelta(minutes=1)),
            args=[]
        )
        jobs_id.append(job.id)

        return jobs_id

    async def event(self, text: str, url: str, channel_id: int):
        channel = self.bot.get_channel(channel_id)
        await channel.send(f"{text}\n\n{url}")

    async def remove_from_db(self):
        self.db.delete_by_expired_time("all_events_by_time")

    def remove_by_id(self, id_):
        doc = self.db.delete("Events", id_)
        for job in doc['data']['jobs']:
            self.sched.remove_job(job)
        return doc
