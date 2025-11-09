from sqlalchemy.orm import Session
import datetime


from models.data_models import City


def create_city(session: Session, city_name: str) -> City:
    
    existing_city = session.query(City).filter_by(name=city_name).first()

    if existing_city:
        existing_city.last_fetched = datetime.date.today()
        session.flush()
        return existing_city
    
    new_city = City(name=city_name)

    session.add(new_city)
    session.flush()
    return new_city
