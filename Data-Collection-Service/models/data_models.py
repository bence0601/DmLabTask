import os
import datetime
import logging

from sqlalchemy import create_engine, Column,Integer,String,Date,Float,ForeignKey,text,Boolean
from sqlalchemy.orm import DeclarativeBase,relationship,Mapped, mapped_column

import services.preseeder

DATABASE_URL = os.getenv("DATABASE_URL") 
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)

logger = logging.getLogger(__name__)  

class Base(DeclarativeBase): ## In the docs of declarative_base, it says this is the newer version, which serves the same purpose, but it will work better with type checkers
    pass

class City(Base):
    __tablename__ = 'cities'  

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(100),nullable=False,unique=True)
    last_fetched : Mapped[datetime.date] = mapped_column(Date,nullable=False,server_default=text("CURRENT_DATE")) ## It automatically fill the col with current date on db-side
    data_days_count : Mapped[int] = mapped_column(Integer, default=0)

    weather_data: Mapped[list["WeatherData"]] = relationship("WeatherData",back_populates="city",cascade="all, delete-orphan") ## forward reference for WeatherData

class WeatherData(Base):
    __tablename__ = 'weather_per_days'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('cities.id'), nullable=False)
    date:  Mapped[datetime.date] = mapped_column(Date, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False) ## celsius
    wind: Mapped[float] = mapped_column(Float, nullable=False) ## km/h
    humidity: Mapped[float] = mapped_column(Float, nullable=False) ## percentage
    precipitation: Mapped[float] = mapped_column(Float, nullable=False) ## mm

    city: Mapped[City] = relationship("City",back_populates="weather_data")


class SeedStatus(Base):
    __tablename__ = "seed_status"

    id: Mapped[int] = Column(Integer, primary_key=True)
    seeded: Mapped[bool] = Column(Boolean, default=False,nullable=False)


def _init_db():
    Base.metadata.create_all(engine)
    logger.info("Database initialized")

if __name__ == "__main__":
    _init_db()
    services.preseeder._preseed_database(engine)
    