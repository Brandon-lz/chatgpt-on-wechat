from .models import database


def init_db():
    database.bind(provider='sqlite', filename='database.db', create_db=True)
    database.generate_mapping(create_tables=True)


