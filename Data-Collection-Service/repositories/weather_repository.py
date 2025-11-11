import datetime
import random
import logging

from typing import Tuple, List

from sqlalchemy.orm import Session

from models.data_models import WeatherData

logger = logging.getLogger(__name__)


def create_weather_data(
    session: Session, weather_model: WeatherData
) -> None:
    return session.add(weather_model)


def check_existing_weather_data_for_city(
    session: Session, city_id: int
) -> WeatherData | None:
    today = datetime.date.today()

    return (
        session.query(WeatherData)
        .filter(WeatherData.city_id == city_id, WeatherData.date == today)
        .first()
    )


def get_30_weather_data_for_city(
    session: Session, city_id: int
) -> Tuple[List[float], List[float], List[float]] | int:
    days_count = (
        session.query(WeatherData).filter(WeatherData.city_id == city_id).count()
    )
    if days_count < 30:
        return days_count

    rows = (
        session.query(WeatherData.temperature, WeatherData.humidity, WeatherData.wind)
        .filter(WeatherData.city_id == city_id)
        .order_by(WeatherData.date.asc())
        .all()
    )
    if not rows:
        return 0

    temps, hums, winds = zip(*rows)
    return list(temps), list(hums), list(winds)


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
