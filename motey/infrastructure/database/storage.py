from typing import Optional

from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from motey.infrastructure.database.tables import Emote
from motey.infrastructure.database.tables import User


class EmoteStorage:
    def __init__(self, session: Session):
        self._session = session

    def fetch_all_emotes(self) -> List[Emote]:
        return self._session.scalars(select(Emote)).all()

    def emote_exists(self, name: str) -> bool:
        return self._session.query(exists().where(Emote.name == name)).scalar()

    def add_emote(self, name: str, path: str, author: User) -> None:
        emote = Emote(name=name, path=path, author=author)
        self._session.add(emote)
        self._session.commit()

    def get_emote_by_name(self, name: str) -> Optional[Emote]:
        stmt = select(Emote).where(Emote.name == name)
        try:
            return self._session.scalars(stmt).one()
        except:
            return None
