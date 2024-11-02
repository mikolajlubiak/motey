from sqlalchemy import (
    Table,
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import List, Optional


class Base(DeclarativeBase):
    pass


def create_association_table(name: str, column1: str, column2: str) -> Table:
    return Table(
        name,
        Base.metadata,
        Column(f"{column1}_id", ForeignKey(f"{column1}s.id"), primary_key=True),
        Column(f"{column2}_id", ForeignKey(f"{column2}s.id"), primary_key=True),
    )


users_servers_association_table = create_association_table(
    "users_servers_association_table", "server", "user"
)
admins_servers_association_table = create_association_table(
    "admins_servers_association_table", "server", "user"
)
emotes_servers_association_table = create_association_table(
    "emotes_servers_association_table", "server", "emote"
)


class Server(Base):
    __tablename__ = "servers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    guild: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)

    server_users: Mapped[List["User"]] = relationship(
        back_populates="user_servers", secondary=users_servers_association_table
    )

    server_admins: Mapped[List["User"]] = relationship(
        back_populates="admin_servers", secondary=admins_servers_association_table
    )

    server_emotes: Mapped[List["Emote"]] = relationship(
        back_populates="emote_servers", secondary=emotes_servers_association_table
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    user_emotes: Mapped[Optional[List["Emote"]]] = relationship(back_populates="author")
    replace: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_servers: Mapped[Optional[List["Server"]]] = relationship(
        back_populates="server_users", secondary=users_servers_association_table
    )

    admin_servers: Mapped[Optional[List["Server"]]] = relationship(
        back_populates="server_admins", secondary=admins_servers_association_table
    )


class Emote(Base):
    __tablename__ = "emotes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="user_emotes")
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    path: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    emote_servers: Mapped[Optional[List["Server"]]] = relationship(
        back_populates="server_emotes", secondary=emotes_servers_association_table
    )
