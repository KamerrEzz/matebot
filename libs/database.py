# -*- coding: utf-8 -*-

import logging
import functools
from faunadb import query as q
from faunadb.client import FaunaClient
#from faunadb.objects import Ref

log = logging.getLogger(__name__)

def log_debug(func):
    """
    Ejemplo de implementación de un decorator
    """
    # Preserva la información de la función original
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        log.info("%s%s\n%s", func.__name__, args[1:], value)
        return value
    return wrapper

class Database:
    """Clase utilizada para definir querys

    Para obtener el id de un documento:
    doc["ref"].id()
    """
    def __init__(self, secret):
        self.q = q
        self.client = FaunaClient(secret=secret)

    def inicialize(self):
        """Creo la colección e índices utilizados"""

        # Creo la colección
        self.client.query(
            q.create_collection({
                "name": "Events",
            })
        )

        # Creo un indice general para buscar todos los documentos
        self.client.query(
            q.create_index(
                {
                    "name": "all_events",
                    "source": q.collection("Events")
                }
            )
        )

        # Creo un indice para buscar todos los documentos
        # que contengan el campo time
        self.client.query(
            q.create_index(
                {
                    "name": "all_events_by_time_range",
                    "source": q.collection("Events"),
                    "values": [
                        {"field": ["data", "time"]},
                        {"field": ["ref"]}
                    ]
                }
            )
        )

    def create(self, collection, data):
        """Creo un documento en una colección existente

        create("my_collection", {"name": "John", "age": 30})
        """
        return self.client.query(
            q.create(
                q.collection(collection),
                {"data": data}
            )
        )

    def get(self, collection, id_):
        """Obtiene un documento de una colección por el id

        get("my_collection", 1234567890)
        """
        return self.client.query(
            q.get(
                q.ref(q.collection(collection), id_)
            )
        )

    def get_all(self, index):
        """Obtiene todos los documentos que hacen match con el index

        get_all("my_index")
        """
        return self.client.query(
            q.map_(
                lambda ref: q.get(ref),
                q.paginate(q.match(q.index(index)))
            )
        )

    def get_by_expired_time(self, index):
        """Obtengo todos los documentos con fechas anteriores a la actual

        get_by_expired_time("my_index")
        """
        return self.client.query(
            q.map_(
                lambda _, ref: q.get(ref),
                q.paginate(
                    q.range(
                        q.match(q.index(index)), q.time("2020-01-01T00:00:00Z"), q.now()
                    )
                )
            )
        )

    def update(self, collection, id_, data):
        """Actualiza datos

        Actualiza los datos dentro de un documento, pero mantiene los
        campos que no estan definidos en los nuevos datos

        update("my_collection", 1234567890, {"name": "John", "age": 30})
        """
        return self.client.query(
            q.update(
                q.ref(q.collection(collection), id_),
                {"data": data}
            )
        )

    def update_all_jobs(self, collection, array_data):
        """Actualiza los jobs

        Actualizo todos los datos jobs en todos los documentos
        """
        # array_data = [(ref_id, {"jobs": jobs})]
        return self.client.query(
            q.map_(
                lambda ref, data: q.update(
                    q.ref(q.collection(collection), ref), {"data": data}
                ),
                array_data
            )
        )

    def replace(self, collection, id_, data):
        """Reemplaza datos

        Reemplaza los datos existentes de un documento dentro de una
        colección

        replace("my_collection", 1234567890, {"name": "John", "age": 30})
        """
        return self.client.query(
            q.replace(
                q.ref(q.collection(collection), id_),
                {"data": data}
            )
        )

    def delete(self, collection, id_):
        """Elimino un documento por el id

        delete("my_collection", 1234567890)
        """
        return self.client.query(
            q.delete(
                q.ref(q.collection(collection), id_)
            )
        )

    def delete_by_expired_time(self, index):
        """Elimino todos los documentos que caducaron

        delete_by_expired_time("my_index")
        """
        return self.client.query(
            q.map_(
                lambda _, ref: q.delete(ref),
                q.paginate(
                    q.range(
                        q.match(q.index(index)), q.time("2020-01-01T00:00:00Z"), q.time_add(q.now(), 1, "minutes")
                    )
                )
            )
        )
