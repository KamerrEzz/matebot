# -*- coding: utf-8 -*-

import os
import logging
import functools
from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from libs.database import Database as DB

log = logging.getLogger(__name__)

# def my_decorator_name(name):
#     def my_custome_decorator(function):
#         def wrapper(*args, **kwargs):
# 
#             print('Name:', name)
#             return function(*args, **kwargs)
# 
#         return wrapper
# 
#     return my_custome_decorator

class Reminder:
    def __init__(self, secret):
        # Accedo a la base de datos
        self.db = DB(secret)

        # Arranco en Async Scheduler
        self.sched = AsyncIOScheduler()
        self.sched.start()

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if not callable(value):
            raise ValueError("The value must be a function")
        self._action = value

    @property
    def reminders(self):
        return self._reminders

    @reminders.setter
    def reminders(self, value):
        if not isinstance(value, list):
            raise ValueError("The value must be a list")
        self._reminders = value

    # Funciones publicas

    async def add(self, author, url, date, time, time_zone, channel_id):
        """
        Agrega un nuevo evento y crea los jobs de los recordatorios
        """
        try:
            date_time = datetime.fromisoformat(f"{date}T{time}{time_zone}")
            date_time_now = datetime.utcnow().replace(tzinfo=timezone.utc)

            # Si la fecha del evento es anterior a la actual salgo
            if date_time < date_time_now:
                return []

            # channel_id == <#192393930203>
            # capturo solo el número channel_id[2:][:-1] == 192393930203
            event = self._generate_event(author, url, date_time, channel_id[2:][:-1])
            jobs_id = self._create_jobs(event)

            # Guardo el evento en la base de datos
            data = {
                "author": event['author'],
                "url": event['url'],
                "time": self.db.q.time(event['time'].isoformat()),
                "channel": event['channel'],
                "jobs": jobs_id
            }

            # Genero un registro local
            return self.db.create("Events", data)

        except:
            pass

    async def load(self):
        """
        Se utiliza para cargar los eventos que están guardados en la base de
        datos al momento de inciar el programa.

        Lee los eventos de la base de datos, los carga en el scheduler y
        actuliza la base de datos con los nuevos jobs_id

        """
        docs = self.db.get_all("all_events")
        new_docs = []
        for doc in docs['data']:
            event = {
                "url":       doc['data']['url'],
                "time":      datetime.fromisoformat(f"{doc['data']['time'].value[:-1]}+00:00"),
                "channel":   doc['data']['channel'],
                "reminders": self.reminders
            }

            # Creo los jobs
            jobs_id = self._create_jobs(event)
            new_docs.append((doc['ref'].id(), {"jobs": jobs_id}))

        # Actulizo la base de datos con los nuevos jobs_id
        return self.db.update_all_jobs("Events", new_docs)

    async def list(self):
        """
        Lista todos los eventos programados
        """
        events = self.db.get_all("all_events")
        return events['data']

    async def remove(self, id_):
        """
        Borro un evento programado
        """
        return self._remove_by_id(id_)

    # Funciones privadas

    def _remove_by_id(self, id_):
        doc = self.db.delete("Events", id_)
        for job in doc['data']['jobs']:
            self.sched.remove_job(job)
        return doc

    async def _remove_old_event(self):
        self.db.delete_by_expired_time("all_events_by_time")

    def _create_jobs(self, event):
        dt_event = event['time']
        dt_now = datetime.utcnow().replace(tzinfo=timezone.utc)

        jobs_id = []
        for reminder in event['reminders']:
            if dt_event > dt_now + reminder['delta']:
                log.info("Added event")
                job = self.sched.add_job(
                    self.action,
                    'date',
                    run_date=(dt_event - reminder['delta']),
                    args=[reminder['message'], event['url'], event['channel']]
                )
                jobs_id.append(job.id)

        # Job para eliminar el registro de la base de datos
        job = self.sched.add_job(
            self._remove_old_event,
            'date',
            run_date=(dt_event),
            args=[]
        )
        jobs_id.append(job.id)

        return jobs_id

    def _generate_event(self, author, url, date_time, channel_id):
        return {
            "author": f"{author}",
            "url": url,
            "time": date_time,
            "channel": int(channel_id),
            "reminders": self.reminders
        }
