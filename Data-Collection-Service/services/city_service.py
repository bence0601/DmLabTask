import logging

from repositories import city_repository
from repositories.city_repository import Session
from models.data_models import engine

logger = logging.getLogger(__name__)


class CityService:

    @staticmethod
    def add_city_data(data) -> int:
        with Session(engine) as session, session.begin():
            new_city = city_repository.add_city(session, data)
            session.flush()
            city_id = new_city.id
            return city_id

    @staticmethod
    def check_existing_city(data) -> int | None:
        with Session(engine) as session, session.begin():
            existing_city = city_repository.check_existing_city(session, data)
            if existing_city:
                return existing_city.id
            return None
