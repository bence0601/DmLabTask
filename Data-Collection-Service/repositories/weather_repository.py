import datetime
import random

from sqlalchemy.orm import Session

from models.data_models import WeatherData,City


def create_weather_data(session:Session, city_id:int) -> int:

    today = datetime.now().date()

    weather_records = []
    for days_ago in range(30, -1, -1):
        day = today - datetime.timedelta(days=days_ago)

        weather = WeatherData(
            city_id=city_id,
            date=day,
            temperature=round(random.uniform(-5, 30), 1),
            wind=round(random.uniform(0, 50), 1),
            humidity=round(random.uniform(20, 95), 1),
            precipitation=round(random.uniform(0, 20), 1),
        )
        weather_records.append(weather)

    if weather_records:
        session.add_all(weather_records)
    
    city = session.get(City,city_id)
    city.data_days_count = len(weather_records)

    return len(weather_records)
