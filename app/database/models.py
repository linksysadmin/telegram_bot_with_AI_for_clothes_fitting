import datetime
from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import as_declarative, Mapped, mapped_column, relationship


datetime = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.now())]


@as_declarative()
class Base:
    pass


class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    available_generations: Mapped[int] = mapped_column(default=5)
    used_generations: Mapped[int] = mapped_column(default=0)
    datetime_registration: Mapped[datetime]

    payments: Mapped[list["PaymentsORM"]] = relationship()


class PaymentsORM(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    total_amount: Mapped[float]
    generations: Mapped[int]
    datetime: Mapped[datetime]

    users: Mapped[list["UsersORM"]] = relationship(overlaps="payments")

