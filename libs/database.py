# -*- coding: utf-8 -*-

import logging
from faunadb import query as q
from faunadb.client import FaunaClient
#from faunadb.objects import Ref

log = logging.getLogger(__name__)

# Ejemplo de implementación de un decorators
def log_debug(f):
    def wrapper(*args, **kwargs):
        d = f(*args, **kwargs)
        log.info(f"{f.__name__}{args[1:]}\n{d}")
        return d
    return wrapper

class Database:
    """
    Para obtener el id de un documento:

    doc["ref"].id()

    """
    def __init__(self, secret):
        self.q = q
        self.client = FaunaClient(secret=secret)

    def create(self, collection, data):
        """
        Creo un documento en una colección existente

        create("my_collection", {"name": "John", "age": 30})
        """
        return self.client.query(
            q.create(
                q.collection(collection),
                {"data": data}
            )
        )

    def get(self, collection, id_):
        """
        Obtiene un documento de una colección por el id
        """
        d = self.client.query(
            q.get(
                q.ref(q.collection(collection), id_)
            )
        )
        log.debug(f"get: {d}")
        return d

    @log_debug
    def get_all(self, index):
        """
        Obtiene todos los documentos que hacen match con el index
        """
        return self.client.query(
            q.map_(
                lambda x: q.get(x),
                q.paginate(q.match(q.index(index)))
            )
        )

    def update(self, collection, id_, data):
        """
        Actualiza los datos de una colección, pero mantiene los campos que no
        estan definidos en los nuevos datos
        """
        return self.client.query(
            q.update(
                q.ref(q.collection(collection), id_),
                {"data": data}
            )
        )

    def replace(self, collection, id_, data):
        """
        Reemplaza los datos existentes de un documento dentro de una
        colección
        """
        return self.client.query(
            q.replace(
                q.ref(q.collection(collection), id_),
                {"data": data}
            )
        )
