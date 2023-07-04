from typing import List, Optional

from sqlalchemy import Connection, insert, select, Row
from sqlalchemy.exc import IntegrityError

from motey.infrastructure.database import tables
from motey.infrastructure.database.tables import emotes
from motey.domain.read_models import Emote


class StorageException(Exception):
    pass


class EmoteStorage:
    def __init__(self, connection: Connection):
        self._connection = connection

    def fetch_all_emotes(self) -> List[Emote]:
        cursor = self._connection.execute(emotes.select())
        records = cursor.all()
        return (self._convert_record_to_emote(record) for record in records)

    def emote_exists(self, name: str) -> bool:
        cursor = self._connection.execute(emotes.select().where(emotes.c.name==name))
        record = cursor.one_or_none()
        return record is not None

    def add_emote(self, name: str, location: str, login: str) -> None:
        statement = select(users.c.id)\
            .where(users.c.login==login)
        try:
            user_id = self._connection.execute(statement).one()
        except IntegrityError as e:
            raise StorageException from e
        statement = insert(emotes) \
            .values(name=name, location=location, user_id=user_id)
        try:
            self._connection.execute(statement)
            self._connection.commit()
        except IntegrityError as e:
            raise StorageException from e

    def get_emote_by_name(self, name: str) -> Optional[Emote]:
        cursor = self._connection.execute(select(emotes).where(emotes.c.name==name))
        record = cursor.one_or_none()
        if not record:
            return
        return self._convert_record_to_emote(record)

    def increase_emote_usage_count(self, emote_id: int) -> None:
        statement = emotes.update().where(emotes.c.id==emote_id).values(times_used=emotes.c.times_used + 1)
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

