from sqlalchemy import (
        Table,
        Column,
        Integer,
        BigInteger,
        String,
        Boolean,
        ForeignKey
        )
from sqlalchemy.orm import (
        DeclarativeBase,
        Mapped,
        mapped_column,
        relationship
)
from typing import List, Optional

class Base(DeclarativeBase):
        pass

users_servers_association_table = Table(
    "users_servers_association_table",
    Base.metadata,
    Column("server_id", ForeignKey("servers.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

admins_servers_association_table = Table(
    "admins_servers_association_table",
    Base.metadata,
    Column("server_id", ForeignKey("servers.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

emotes_servers_association_table = Table(
    "emotes_servers_association_table",
    Base.metadata,
    Column("server_id", ForeignKey("servers.id"), primary_key=True),
    Column("emote_id", ForeignKey("emotes.id"), primary_key=True),
)
    
class Server(Base):
        __tablename__ = "servers"
        name: Mapped[str] = mapped_column(String(32), nullable=False)
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        guild: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        server_users: Mapped[List["User"]] = relationship(back_populates="user_servers", secondary=users_servers_association_table)
        server_admins: Mapped[List["User"]] = relationship(back_populates="admin_servers", secondary=admins_servers_association_table)
        server_emotes: Mapped[List["Emote"]] = relationship(back_populates="emote_servers", secondary=emotes_servers_association_table)

class User(Base):
        __tablename__ = "users"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        user_servers: Mapped[Optional[List["Server"]]] = relationship(back_populates="server_users", secondary=users_servers_association_table)
        admin_servers: Mapped[Optional[List["Server"]]] = relationship(back_populates="server_admins", secondary=admins_servers_association_table)
        user_emotes: Mapped[Optional[List["Emote"]]] = relationship(back_populates="author")
        replace: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
        banned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class Emote(Base):
        __tablename__ = "emotes"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
        author: Mapped["User"] = relationship(back_populates="user_emotes")
        emote_servers: Mapped[Optional[List["Server"]]] = relationship(back_populates="server_emotes", secondary=emotes_servers_association_table)
        name: Mapped[str] = mapped_column(String(32), nullable=False)
        path: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
