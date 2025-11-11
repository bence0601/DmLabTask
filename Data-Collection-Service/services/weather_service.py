import logging
from sqlalchemy.orm import Session
from models.data_models import engine
from repositories import weather_repository

logger = logging.getLogger(__name__)


class WeatherService:
    @staticmethod
    def add_weather_data(weather_model):
        with Session(engine) as session, session.begin():
            weather = weather_repository.create_weather_data(session, weather_model)
            return weather

    @staticmethod
    def get_weather_for_30_days(city_id):
        with Session(engine) as session, session.begin():
            return weather_repository.get_30_weather_data_for_city(session, city_id)
