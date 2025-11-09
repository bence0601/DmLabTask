from sqlalchemy.orm import Session
import datetime


from models.data_models import City,WeatherData


def create_city(session: Session, city_name: str) -> City | None:

    existing_city = session.query(City).filter_by(name=city_name).first()

    if existing_city:
        today = datetime.date.today()
        existing_weather_for_date = session.query(WeatherData).filter(
            WeatherData.city_id == existing_city.id,
            WeatherData.date == today
        ).first()
        
        if existing_weather_for_date:
            return None
        else:
            existing_city.last_fetched = today
            session.flush()
            return existing_city

    new_city = City(name=city_name)
    session.add(new_city)
    session.flush()
    return new_city
