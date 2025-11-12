import os
import logging
import datetime

from sqlalchemy import Integer, Date, create_engine, Float, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, echo=True)

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class ForecastModel(Base):
    __tablename__ = "forecast"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    wind: Mapped[float] = mapped_column(Float, nullable=True)
    humidity: Mapped[float] = mapped_column(Float, nullable=True)


def init_db():
    Base.metadata.create_all(engine)
    logger.info("Database initialized")


if __name__ == "__main__":
    init_db()
