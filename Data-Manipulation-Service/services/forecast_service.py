import os
import logging
import datetime
from repositories.forecast_repository import (
    add_forecast,
    get_forecast_for_city_and_date,
    Session,
)
from models.forecast import ForecastModel, engine
from mappers.forecast_mapper import model_to_dto
from dtos.forecast_dto import ForecastDTO

logger = logging.getLogger(__name__)


class ForecastService:

    @staticmethod
    def check_existing_forecast(city: str) -> ForecastDTO | None:
        today = datetime.date.today()
        with Session(engine) as session:
            existing_forecast = get_forecast_for_city_and_date(session, city, today)
            if existing_forecast is not None:
                return model_to_dto(existing_forecast)
            else:
                return None

    @staticmethod
    def create_forecast_for_city(json) -> ForecastDTO:
        data = json.get("data", {})
        _temp = data.get("temperatures", [])
        _humidity = data.get("humidity", [])
        _wind = data.get("wind_speeds", [])
        _city_name = data.get("city")

        avg_temp = sum(_temp) / len(_temp) if _temp else 0
        avg_humidity = sum(_humidity) / len(_humidity) if _humidity else 0
        avg_wind = sum(_wind) / len(_wind) if _wind else 0

        new_forecast = ForecastModel(
            city=_city_name,
            date=datetime.date.today(),
            temperature=avg_temp,
            wind=avg_wind,
            humidity=avg_humidity,
        )

        with Session(engine) as session, session.begin():
            add_forecast(session, new_forecast)
            session.flush()
            forecast_dto = model_to_dto(new_forecast)

        return forecast_dto
