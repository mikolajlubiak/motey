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

association_table = Table(
    "association_table",
    Base.metadata,
    Column("server_id", ForeignKey("servers.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)
    
class Server(Base):
        __tablename__ = "servers"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        guild: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        server_users: Mapped[List["User"]] = relationship(back_populates="user_servers", secondary=association_table)
        replace: Mapped[bool] = mapped_column(Boolean, nullable=False)
        banned: Mapped[bool] = mapped_column(Boolean, nullable=False)

class User(Base):
        __tablename__ = "users"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        user_servers: Mapped[List["Server"]] = relationship(back_populates="server_users", secondary=association_table)
        user_emotes: Mapped[List["Emote"]] = relationship(back_populates="author")
        replace: Mapped[bool] = mapped_column(Boolean, nullable=False)
        banned: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Emote(Base):
        __tablename__ = "emotes"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
        author: Mapped["User"] = relationship(back_populates="user_emotes")
        name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
        path: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
