from sqlalchemy.orm import Session

from models.data_models import City


def add_city(session: Session, city_model: City) -> City:
    session.add(city_model)
    return city_model


def check_existing_city(session: Session, city_name: str) -> City | None:
    return session.query(City).filter_by(name=city_name).first()
