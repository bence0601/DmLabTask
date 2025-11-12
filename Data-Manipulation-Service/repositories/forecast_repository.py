import datetime
import logging

from sqlalchemy.orm import Session

from models.forecast import ForecastModel

logger = logging.getLogger(__name__)


def get_forecast_for_city_and_date(
    session: Session, city_name: str, date: datetime.date
) -> ForecastModel | None:
    return (
        session.query(ForecastModel)
        .filter(ForecastModel.city == city_name, ForecastModel.date == date)
        .first()
    )


def add_forecast(session: Session, forecast_to_add: ForecastModel) -> ForecastModel:
    session.add(forecast_to_add)
    return forecast_to_add
