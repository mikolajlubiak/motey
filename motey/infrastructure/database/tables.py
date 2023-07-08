from sqlalchemy import (
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
    
class Server(Base):
        __tablename__ = "servers"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        guild: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        server_users: Mapped[List["User"]] = relationship(back_populates="user_servers")
        replace: Mapped[bool] = mapped_column(Boolean, nullable=False)
        banned: Mapped[bool] = mapped_column(Boolean, nullable=False)

class User(Base):
        __tablename__ = "users"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        user_servers: Mapped[List["Server"]] = relationship(back_populates="server_users")
        replace: Mapped[bool] = mapped_column(Boolean, nullable=False)
        banned: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Emote(Base):
        __tablename__ = "emotes"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        author: Mapped["User"] = relationship("User")
        name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
        path: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
