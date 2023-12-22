from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .models import Transaction
from datetime import date
from typing import Any


def add_raw_transaction(
    tr_description: str,
    tr_memo: str,
    tr_amount: float,
    tr_date: date,
    tr_account_id: int,
    session: Session,
) -> None:
    tr = Transaction(
        description=tr_description,
        memo=tr_memo,
        amount=tr_amount,
        date=tr_date,
        account_id=tr_account_id,
    )

    try:
        session.add(tr)
        session.commit()
    except IntegrityError:
        print("Error catched!")
        session.rollback()


def get_transaction(id: int, session: Session) -> Transaction:
    return session.get(Transaction, id)
    return session.execute(
        select(Transaction).where(Transaction.id == id)
    ).scalar_one_or_none()


def delete_transaction(id: int, session: Session) -> None:
    tr = get_transaction(id, session)
    if tr is not None:
        session.delete(tr)
        session.commit()


def update_transaction(id: int, new_values: dict, session: Session) -> None:
    """Update transaction

    :param id: Primary key of transaction
    :type id: int
    :param new_values: key:value pair of values to update
    :type new_values: dict
    :param session: session
    :type session: Session
    """
    tr = get_transaction(id, session)

    if tr is not None:
        for k, v in new_values.items():
            if hasattr(tr, k):
                setattr(tr, k, v)
            else:
                print(f"Attribute {k} doesn't exist")

        session.commit()
    else:
        print(f"Transaction with id {id} not found")
