from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

connection_string = os.getenv("DB_CONNECTION")
if not connection_string:
    raise ValueError("DB_CONNECTION környezeti változó nincs beállítva.")
print(connection_string)
engine = create_engine(connection_string)

Base = declarative_base()

class City(Base):
    __tablename__ = 'cities'  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(100), nullable=False, unique=True)
    
    weather_data = relationship("WeatherData", back_populates="city")
    weather_data_aggregated = relationship("AggregatedWeatherData", back_populates="city")

class WeatherData(Base):
    __tablename__ = 'weatherdata'  
    
    id = Column(Integer, primary_key=True, autoincrement=True) 
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)  
    date = Column(Date, nullable=False) 
    hour = Column(Integer, nullable=False)  
    temp_c = Column(DECIMAL, nullable=False) 
    wind_mph = Column(DECIMAL, nullable=False)  
    precip_mm = Column(DECIMAL, nullable=False)  
    
  
    city = relationship("City", back_populates="weather_data")


class AggregatedWeatherData(Base):
    __tablename__ = 'aggregatedweatherdata' 
    
    id = Column(Integer, primary_key=True, autoincrement=True)  
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date = Column(Date, nullable=False)  
    
   
    max_temp_c = Column(DECIMAL, nullable=False)
    min_temp_c = Column(DECIMAL, nullable=False)
    avg_temp_c = Column(DECIMAL, nullable=False)
    min_wind_mph = Column(DECIMAL, nullable=False)
    max_wind_mph = Column(DECIMAL, nullable=False)
    avg_wind_mph = Column(DECIMAL, nullable=False)
    min_precip_mm = Column(DECIMAL, nullable=False)
    max_precip_mm = Column(DECIMAL, nullable=False)
    avg_precip_mm = Column(DECIMAL, nullable=False)
    
    
    city = relationship("City", back_populates="weather_data_aggregated")


Base.metadata.create_all(engine)