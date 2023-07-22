from typing import Optional, List

from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy import func

from motey.infrastructure.database.tables import Emote, Server, User


class EmoteStorage:
    def __init__(self, database):
        self._db = database

    def fetch_all_emotes(self) -> List[Emote]:
        with Session(self._db) as db_session:
            return db_session.scalars(select(Emote)).all()

    def emote_exists(self, name: str) -> bool:
        with Session(self._db) as db_session:
            return db_session.query(exists().where(Emote.name == name)).scalar()

    def add_emote(self, name: str, path: str, author: User) -> None:
        emote = Emote(name=name, path=path, author=author)
        with Session(self._db) as db_session:
            db_session.add(emote)
            db_session.commit()

    def get_emote_by_name(self, name: str) -> Optional[Emote]:
        stmt = select(Emote).where(Emote.name == name)
        with Session(self._db) as db_session:
            try:
                return db_session.scalars(stmt).one()
            except:
                return None

class UserStorage:
    def __init__(self, database):
        self._db = database

    def get_user_servers(self, discord_id: int) -> List[Server]:
        stmt = select(User).where(User.discord_id == discord_id)
        with Session(self._db) as db_session:
            user = db_session.scalars(stmt).one()
            try:
                return user.user_servers
            except:
                return None
