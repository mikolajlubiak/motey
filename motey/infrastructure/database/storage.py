from typing import Optional, List

from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy import func

from motey.infrastructure.database.tables import Emote, Server, User


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

    def get_emote_by_name(self, name: str, server_id: str) -> Optional[Emote]:
        stmt = select(Emote).join(Emote.emote_servers).where(Emote.name == name, Server.id.contains(server_id))
        try:
            return self._session.scalars(stmt).one()
        except:
            return None
class UserStorage:
    def __init__(self, session: Session):
        self._session = session

    def get_user_servers(self, discord_id: str) -> List[Server]:
        stmt = select(User).where(User.discord_id == discord_id)
        user = self._session.execute(stmt).scalar()
        try:
            return user.user_servers
        except:
            return None