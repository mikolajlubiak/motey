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
    Column('login', VARCHAR(12), nullable=False, unique=True),
    Column('password', VARCHAR(512), nullable=False),
    Column('created_at', DATETIME, server_default=func.current_timestamp())
)


emotes = Table(
    'emotes', meta,
    Column('id', BIGINT, primary_key=True, autoincrement=True),
    Column('name', VARCHAR(12), nullable=False, unique=True,),
    Column('location', VARCHAR(128), nullable=False, unique=True),
    Column('times_used', BIGINT, default=0),
    Column('created_at', DATETIME, server_default=func.current_timestamp()),
    Column('user_id', BIGINT, ForeignKey('users.id'))
)


all_tables = [users, emotes]
