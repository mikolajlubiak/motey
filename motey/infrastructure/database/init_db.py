from sqlalchemy import MetaData

from motey.infrastructure.database.tables import all_tables
from motey.infrastructure.database.engine import get_db


def _create_tables(engine) -> None:
    MetaData().create_all(bind=engine, tables=all_tables)


def init_db() -> None:
    _create_tables(get_db())


if __name__ == '__main__':
    init_db()
