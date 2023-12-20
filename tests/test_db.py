from plutus.db.models import Base, Transaction
from datetime import date, datetime, timedelta, UTC
import pytest
from plutus.db.utils import *
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


def test_create_raw_transaction(db_session):
    new_transaction = Transaction(
        description="test",
        memo="",
        amount=100.0,
        date=date(2023, 12, 4),
        account_id=2,
    )

    db_session.add(new_transaction)
    db_session.commit()

    assert new_transaction.id is not None


def test_get_no_transaction(db_session):
    tr = get_transaction(1000, db_session)
    assert tr is None


def test_transaction_defaults(db_session):
    new_transaction = Transaction(
        description="test",
        memo="",
        amount=100.0,
        date=date(2023, 12, 4),
        account_id=2,
    )

    db_session.add(new_transaction)
    db_session.commit()

    # Retrieve the user from the database
    tr = db_session.execute(
        select(Transaction).where(Transaction.description == "test")
    ).scalar_one()

    assert tr is not None
    assert tr.cleaned == False
    assert abs(tr.timestamp - datetime.now(UTC).replace(tzinfo=None)) < timedelta(
        seconds=1
    )


def test_adding_duplicate_transaction(db_session):
    add_raw_transaction("test", "", 100.0, date(2023, 12, 4), 2, db_session)
    add_raw_transaction("test", "", 100.0, date(2023, 12, 4), 2, db_session)

    trs = db_session.query(Transaction).filter_by(description="test").all()

    assert len(trs) == 1


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
    new_transaction = Transaction(
        description="test",
        memo="",
        amount=100.0,
        date=date(2023, 12, 4),
        account_id=2,
    )

    db_session.add(new_transaction)
    db_session.commit()

    update_transaction(2, {"description": "updated test"}, db_session)

    # Retrieve the user from the database
    tr = get_transaction(1, db_session)

    assert tr is not None
    assert tr.cleaned == False
    assert tr.description == "test"


def test_update_trsnsaction_key_not_exist(db_session):
    new_transaction = Transaction(
        description="test",
        memo="",
        amount=100.0,
        date=date(2023, 12, 4),
        account_id=2,
    )

    db_session.add(new_transaction)
    db_session.commit()

    update_transaction(1, {"invalid": "updated test"}, db_session)

    # Retrieve the user from the database
    tr = get_transaction(1, db_session)

    assert tr is not None
    assert tr.cleaned == False
    assert tr.description == "test"


def test_delete_user(db_session):
    new_transaction = Transaction(
        description="test",
        memo="",
        amount=100.0,
        date=date(2023, 12, 4),
        account_id=2,
    )

    db_session.add(new_transaction)
    db_session.commit()

    delete_transaction(1, db_session)

    tr = get_transaction(1, db_session)

    assert tr is None


def delete_non_existing_transaction(db_session):
    """Check that deleting something that doesn't exist doesn"t throw an exception"""
    delete_transaction(1, db_session)
