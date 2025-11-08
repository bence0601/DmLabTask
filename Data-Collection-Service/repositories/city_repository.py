from sqlalchemy.orm import Session

from models.data_models import City


def create_city(session: Session, city_name: str) -> int:
    new_city = City(name=city_name, data_days_count=0)

    session.add(new_city)
    session.flush()
    return new_city.id
