from flask import Blueprint, jsonify, request
import logging
from services.city_service import CityService
from services.weather_service import WeatherService
from clients.open_weather_client import OpenWeatherClient

from mappers.open_weather_json_to_dto_mapper import WeatherApiToDtoMapper
from mappers.dto_to_data_model_mapper import CityMapper, WeatherDataMapper


logger = logging.getLogger(__name__)

data_collection_bp = Blueprint("data_collection_bp", __name__)


@data_collection_bp.route("/get-data-for-forecast/<city>", methods=["GET"])
def get_existing_weather_for_forecast(city):
    existing_city_id = CityService.check_existing_city(city)

    if existing_city_id is None:
        client = OpenWeatherClient()
        json_data = client.fetch_from_api(city)

        if not json_data:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "City not found in database or Open Weather API",
                        "data": None,
                    }
                ),
                404,
            )

        city_dto = WeatherApiToDtoMapper.extract_city_dto(json_data)
        city_model = CityMapper.to_model(city_dto)
        new_city_id = CityService.add_city_data(city_model)

        weather_dto = WeatherApiToDtoMapper.extract_weather_dto(json_data)
        weather_model = WeatherDataMapper.to_model(weather_dto, new_city_id)
        WeatherService.add_weather_data(weather_model)

        return (
            jsonify(
                {
                    "success": False,
                    "message": "City data fetched from API, but insufficient historical data for forecast (requires at least 30 days)",
                    "data": None,
                }
            ),
            422,
        )

    existing_weather_data = WeatherService.get_weather_for_30_days(existing_city_id)

    if isinstance(existing_weather_data, int):
        return (
            jsonify(
                {
                    "success": False,
                    "message": f"Insufficient data for forecast. Only {existing_weather_data} days available, 30 required",
                    "data": None,
                }
            ),
            422,
        )

    temps, hums, winds = existing_weather_data

    return (
        jsonify(
            {
                "success": True,
                "data": {
                    "temperatures": temps,
                    "humidity": hums,
                    "wind_speeds": winds,
                    "city": city,
                },
            }
        ),
        200,
    )
