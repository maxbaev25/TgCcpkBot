from datetime import datetime
from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    reg_date: Mapped[datetime] = mapped_column(DateTime)
    is_admin: Mapped[bool] = mapped_column(Boolean)


class Subscription(Base):
    __tablename__ = "subscriptions"

    user_id: Mapped[int] = mapped_column(Integer)
    from_station_id: Mapped[int] = mapped_column(BigInteger)
    to_station_id: Mapped[int] = mapped_column(BigInteger)
    origin_date: Mapped[datetime] = mapped_column(DateTime)


class Donaters(Base):
    __tablename__ = "donaters"
    user_id: Mapped[int] = mapped_column(Integer)
    plan_id: Mapped[int] = mapped_column(BigInteger)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
