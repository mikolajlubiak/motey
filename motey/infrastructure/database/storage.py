from typing import List, Optional

from sqlalchemy import Connection, insert, select, Row
from sqlalchemy.exc import IntegrityError

from motey.infrastructure.database import tables
from motey.domain.read_models import Emote


class StorageException(Exception):
    pass


class EmoteStorage:
    def __init__(self, connection: Connection):
        self._connection = connection

    def fetch_all_emotes(self) -> List[Emote]:
        cursor = self._connection.execute(tables.emotes.select())
        records = cursor.fetchall()
        return [self._convert_record_to_emote(record) for record in records]

    def emote_exists(self, name: str) -> bool:
        cursor = self._connection.execute(tables.emotes.select().where(name==name))
        record = cursor.fetchone()
        return record is not None

    def add_emote(self, name: str, location: str) -> None:
        statement = insert(tables.emotes) \
            .values(name=name, location=location)
        try:
            self._connection.execute(statement)
            self._connection.commit()
        except IntegrityError as e:
            raise StorageException from e

    def get_emote_by_name(self, name: str) -> Optional[Emote]:
        cursor = self._connection.execute(select(tables.emotes.c.location).where(name==name))
        record = cursor.one()
        if not record:
            return
        return self._convert_record_to_emote(record)

    def increase_emote_usage_count(self, emote_id: int) -> None:
        statement = tables.emotes.update().where(id==emote_id).values(times_used=tables.emotes.c.times_used + 1)
        self._connection.execute(statement)
        self._connection.commit()

    @staticmethod
    def _convert_record_to_emote(record: Row) -> Emote:
        return Emote(
            id=record[0],
            name=record[1],
            location=record[2],
            times_used=record[3]
        )

