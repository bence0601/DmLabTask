from models.forecast import ForecastModel
from dtos.forecast_dto import ForecastDTO


def model_to_dto(forecast_model: ForecastModel) -> ForecastDTO:
    return ForecastDTO(
        city_name=forecast_model.city,
        temperature=forecast_model.temperature,
        wind=forecast_model.wind,
        humidity=forecast_model.humidity,
    )
