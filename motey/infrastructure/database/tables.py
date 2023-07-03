from sqlalchemy import (
    MetaData,
    Table,
    Column,
    BIGINT,
    DATETIME,
    VARCHAR,
    func,
    ForeignKey
)


meta = MetaData()


users = Table(
    'users', meta,
    Column('id', BIGINT, primary_key=True, autoincrement=True),
    Column('login', VARCHAR(32), nullable=False, unique=True),
    Column('hashed_password', VARCHAR(128), nullable=False),
    Column('salt', VARCHAR(32), nullable=False),
    Column('session_id', VARCHAR(32), unique=True),
    Column('created_at', DATETIME, server_default=func.current_timestamp())
)


emotes = Table(
    'emotes', meta,
    Column('id', BIGINT, primary_key=True, autoincrement=True),
    Column('name', VARCHAR(32), nullable=False, unique=True,),
    Column('location', VARCHAR(64), nullable=False, unique=True),
    Column('times_used', BIGINT, default=0),
    Column('created_at', DATETIME, server_default=func.current_timestamp()),
    Column('user_id', BIGINT, ForeignKey('users.id'))
)


all_tables = [users, emotes]
