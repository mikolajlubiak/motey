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

class Base(DeclarativeBase):
        pass

class User(Base):
        __tablename__ = "users"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        discord_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
        can_replace: Mapped[bool] = mapped_column(Boolean, nullable=False)
        replace: Mapped[bool] = mapped_column(Boolean, nullable=False)
        banned: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Emote(Base):
        __tablename__ = "emotes"

        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        author: Mapped["User"] = relationship("User")
        name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
        path: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
