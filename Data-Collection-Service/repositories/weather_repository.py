import datetime
import random

from sqlalchemy.orm import Session

from models.data_models import WeatherData, City

def create_weather_data(session: Session, weather_model: WeatherData) -> WeatherData:
    session.add(weather_model)
    session.flush()  
    return weather_model

def create_weather_data_for_preseed(session: Session, city_id: int) -> int:

    today = datetime.datetime.now().date()

    weather_records = []
    for days_ago in range(29, -1, -1):
        weather_records.append(
            WeatherData(
                city_id=city_id,
                date=today - datetime.timedelta(days=days_ago),
                temperature=round(random.uniform(-5, 30), 1),
                wind=round(random.uniform(0, 50), 1),
                humidity=round(random.uniform(20, 95), 1),
                )
                )
        
    if weather_records:
        session.add_all(weather_records)

    return len(weather_records)
