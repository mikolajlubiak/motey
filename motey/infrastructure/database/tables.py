from sqlalchemy import (
        MetaData,
        Table,
        Column,
        BIGINT,
        VARCHAR,
        BOOL,
        func,
        ForeignKey
        )


meta = MetaData()


users = Table(
        'users', meta,
        Column('id', BIGINT, primary_key=True, nullable=False),
        Column('discord_id', BIGINT, nullable=False),
        Column('server_id', BIGINT, ForeignKey('servers.id'), nullable=False),
        Column('can_upload', BOOL, nullable=False),
        Column('replace', BOOL, nullable=False),
        )

servers = Table(
        'servers', meta,
        Column('id', BIGINT, primary_key=True, nullable=False),
        Column('guild', BIGINT, nullable=False, unique=True),
        )


emotes = Table(
        'emotes', meta,
        Column('id', BIGINT, primary_key=True, autoincrement=True),
        Column('server_id', BIGINT, ForeignKey('servers.id'), nullable=False),
        Column('discord_id', BIGINT, ForeignKey('users.discord_id'))
        Column('name', VARCHAR(32), nullable=False, unique=True,),
        Column('path', VARCHAR(64), nullable=False, unique=True),
        )


all_tables = [users, emotes, servers]
