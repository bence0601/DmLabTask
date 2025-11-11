import logging

from repositories import city_repository
from repositories.city_repository import Session
from models.data_models import engine

logger = logging.getLogger(__name__)


class CityService:

    @staticmethod
    def add_city_data(data):
        with Session(engine) as session, session.begin():
            new_city = city_repository.create_city(session, data)
            return new_city

    @staticmethod
    def check_existing_city(data):
        with Session(engine) as session, session.begin():
            existing_city = city_repository.check_existing_city(session, data.name)
            return existing_city
