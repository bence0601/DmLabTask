##Standard libs, 3rd party, custom moduls
import os
import logging
from datetime import datetime, timedelta

import requests

from exceptions.custom_exception import (
    ApiKeyNotFound,
    ApiKeyInvalid,
)

from mappers.dto_to_data_model_mapper import CityMapper, WeatherDataMapper
from mappers.open_weather_json_to_dto_mapper import WeatherApiToDtoMapper
from repositories import city_repository, weather_repository
from repositories.city_repository import Session
from models.data_models import engine

logger = logging.getLogger(__name__)


class DataCollector:
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")

    def __init__(self):
        self.weather_data = []

    def fetch_data_for_today(self, city):
        ##If more functions would exist, it would make sense to create a url builder
        url = self.base_url + f"?q={city}&appid={self.api_key}"
        response = requests.get(url, timeout=10)

        ## If this would be for a larger, real-world project, i would move every http related stuff to an api_client.py or something
        if response.status_code == 401:
            raise ApiKeyInvalid(
                "Invalid API key. Please check your OpenWeather API key."
                )

        if response.status_code == 404:
            raise ValueError(
                f"City '{city}' not found. Please check the city name."
                )
        
        response.raise_for_status()

        logger.info(f"Successfully sent request weather data for {city}")

        data = response.json()
        city_dto = WeatherApiToDtoMapper.extract_city_dto(data)
        city_model = CityMapper.to_model(city_dto)

        with Session(engine) as session:
            created_city = city_repository.create_city(session, city_model.name)
            if created_city is None:
                logger.info("There's already data for this city for this date")
                return None
            session.flush()
            weather_dto = WeatherApiToDtoMapper.extract_weather_dto(data)
            weather_model = WeatherDataMapper.to_model(weather_dto, created_city.id)
            weather_repository.create_weather_data(session, weather_model)
            session.commit()
