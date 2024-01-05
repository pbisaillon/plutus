from plutus import config
from .models import *
from .services import *
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

settings = config.Settings()

engine = create_engine(settings.sqlite_dsn)
Session = sessionmaker(bind=engine)


def getsession():
    return Session()


def get_a_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()


def initialize() -> None:
    Base.metadata.create_all(engine)
