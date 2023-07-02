import sqlalchemy
from sqlalchemy import MetaData

from motey.infrastructure.database.tables import all_tables
from motey.infrastructure.database.engine import get_db


def _drop_all_tables(engine) -> None:
    MetaData().drop_all(bind=engine, tables=all_tables)


def _create_tables(engine) -> None:
    MetaData().create_all(bind=engine, tables=all_tables)


def init_db(engine: sqlalchemy.Engine = get_db()) -> None:
    _drop_all_tables(engine)
    _create_tables(engine)


if __name__ == '__main__':
    init_db()
