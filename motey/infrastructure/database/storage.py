from typing import List

from sqlalchemy import Connection, insert
from sqlalchemy.exc import IntegrityError

from motey.infrastructure.database import tables


class StorageException(Exception):
    pass


class EmoteStorage:
    def __init__(self, connection: Connection):
        self._connection = connection

    def fetch_all_emotes(self) -> List:
        cursor = self._connection.execute(tables.emotes.select())
        records = cursor.fetchall()
        emotes = [emote for emote in records]
        return emotes

    def emote_exists(self, name: str) -> bool:
        cursor = self._connection.execute(tables.emotes.select().where(name=name))
        record = cursor.fetchone()
        return record is not None

    def add_emote(self, name: str, location: str):
        statement = insert(tables.emotes) \
            .values(name=name, location=location)
        try:
            self._connection.execute(statement)
            self._connection.commit()
        except IntegrityError as e:
            raise StorageException from e

