from plutus.db import *
from datetime import date, datetime, timedelta, UTC
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()


def test_get_no_transaction(db_session):
    tr = get_transaction(1000, db_session)
    assert tr is None


def test_update_transaction(db_session):
    new_transaction = Transaction(
        description="test",
        memo="",
        amount=100.0,
        date=date(2023, 12, 4),
        account_id=2,
    )

    db_session.add(new_transaction)
    db_session.commit()

    update_transaction(1, {"description": "updated test"}, db_session)

    # Retrieve the user from the database
    # tr = db_session.execute(select(Transaction).where(Transaction.id == 1)).scalar_one_or_none()

    tr = get_transaction(1, db_session)
    assert tr is not None
    assert tr.cleaned == False
    assert tr.description == "updated test"


def test_update_trsnsaction_not_exist(db_session):
    update_transaction(1000, {"description": "updated test"}, db_session)

    # Retrieve the user from the database
    tr = get_transaction(1, db_session)

    assert tr is None
