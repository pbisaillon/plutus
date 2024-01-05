import datetime
from typing import List, Optional
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
    func,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transaction"
    # Unique constraint
    __table_args__ = (
        UniqueConstraint("description", "memo", "amount", "date", "account_id"),
    )

    id = mapped_column(Integer, primary_key=True)
    description: Mapped[str]
    memo: Mapped[str]
    amount: Mapped[float]
    date: Mapped[datetime.date]
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    cleaned: Mapped[bool] = mapped_column(insert_default=False)

    # many to one
    participant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("participant.id"))
    participant: Mapped["Participant"] = relationship()

    account_id: Mapped[Optional[int]] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship()

    # many to many
    categories: Mapped[List["TransactionCategory"]] = relationship()
    tags: Mapped[List["Tag"]] = relationship(secondary="transaction_tag")


# Category is an adjacency list
class Category(Base):
    __tablename__ = "category"

    id = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("category.id"), primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    children = relationship("Category")


class Tag(Base):
    __tablename__ = "tag"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Participant(Base):
    __tablename__ = "participant"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Account(Base):
    __tablename__ = "account"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    type_id: Mapped[int] = mapped_column(ForeignKey("type.id"))
    type: Mapped["Type"] = relationship()


class Type(Base):
    __tablename__ = "type"
    id = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(unique=True)


# Bridge tables
class TransactionCategory(Base):
    __tablename__ = "transaction_category"
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transaction.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"), primary_key=True
    )
    ratio: Mapped[Optional[float]]
    category: Mapped["Category"] = relationship()


association_table = Table(
    "transaction_tag",
    Base.metadata,
    Column("transaction_id", ForeignKey("transaction.id")),
    Column("tag_id", ForeignKey("tag.id")),
)
