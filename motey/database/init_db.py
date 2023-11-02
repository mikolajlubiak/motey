import sqlalchemy

from motey.database.engine import get_db
from motey.database.tables import Base


def init_db(engine: sqlalchemy.Engine = get_db()) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
