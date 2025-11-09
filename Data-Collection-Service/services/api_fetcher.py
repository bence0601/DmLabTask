##Standard libs, 3rd party, custom moduls
import os
import logging
from datetime import datetime, timedelta

import requests

from exceptions.custom_exception import (
    DataCollectionServiceException,
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

    def __init__(self):
        self.weather_data = []
        self.api_key = self._get_api_key()

    @staticmethod
    def _get_api_key() -> str:
        api_key = os.getenv("API_KEY")
        if not api_key:
            logging.error(
                "API Key invalid or missing. Please make sure that you have a correct one!"
            )
            raise ApiKeyNotFound("Api Key not found in environment variables")
        return api_key

    def fetch_data_for_today(self, city):
        ##If more functions would exist, it would make sense to create a url builder
        url = self.base_url + f"?q={city}&appid={self.api_key}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 401:
                raise ApiKeyInvalid(
                    "Invalid API key. Please check your OpenWeather API key."
                )

            if response.status_code == 404:
                raise ValueError(
                    f"City '{city}' not found. Please check the city name."
                )

            response.raise_for_status()

        except DataCollectionServiceException as e:
            logger.error(e)
            raise
        except ValueError as e:
            logger.error(e)
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {city}: {e}")
            raise

        logger.info(f"Successfully fetched weather data for {city}")

        data = response.json()
        city_dto = WeatherApiToDtoMapper.extract_city_dto(data)
        city_model = CityMapper.to_model(city_dto)

        with Session(engine) as session:
            try:
                created_city = city_repository.create_city(session, city_model.name)
                session.flush()

                weather_dto = WeatherApiToDtoMapper.extract_weather_dto(data)
                weather_model = WeatherDataMapper.to_model(weather_dto, created_city.id)
                weather_repository.create_weather_data(session, weather_model)

                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database transaction failed: {e}")
                raise
