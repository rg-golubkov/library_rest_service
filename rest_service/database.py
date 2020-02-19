"""Module for interact with DB
"""
from sqlalchemy import DDL, create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
Base = declarative_base()

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base.query = db_session.query_property()


def init_app(app, default_values=False):
    """initialize database for Flask app

    Args:
        app: instance of Flask-class
        default_values: initialize database with default values
    """
    global engine

    database_uri = app.config.get('DATABASE_URI')
    if database_uri is None:
        raise RuntimeError('DATABASE_URI needs to be set.')

    engine = create_engine(database_uri)
    db_session.configure(bind=engine)

    from .models import Author, Book

    if default_values:
        _insert_default_values(Author, Book)

    Base.metadata.create_all(bind=engine)

    app.teardown_appcontext(shutdown_session)

    if default_values:
        _insert_default_values(Author, Book)


def shutdown_session(exception=None):
    """Remove database sessions at the end of the request
    """
    db_session.remove()


def _insert_default_values(Author: Base, Book: Base):
    """Add after_create handlers for init DB with default values
    """
    event.listen(Author.__table__, 'after_create', DDL('''
        INSERT INTO %(table)s(id, fullname) VALUES
            (1, 'Henry Charles Bukowski'),
            (2, 'Nelle Harper Lee'),
            (3, 'Arthur Conan Doyle')
    '''))

    event.listen(Book.__table__, 'after_create', DDL('''
        INSERT INTO %(table)s(title, publication_year, author_id) VALUES
            ('Post Office', 1971, 1),
            ('Factotum', 1975, 1),
            ('Hollywood', 1989, 1),
            ('To Kill a Mockingbird', 1960, 2),
            ('The Hound of the Baskervilles', 1901, 3),
            ('The Adventure of the Red Circle', 1911, 3)
    '''))
