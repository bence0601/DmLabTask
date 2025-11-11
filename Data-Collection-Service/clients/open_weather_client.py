import os
import requests
import logging
from exceptions.custom_exception import ApiKeyNotFound, ApiKeyInvalid


logger = logging.getLogger(__name__)


class OpenWeatherClient:
    api_key = os.getenv("API_KEY")

    def __init__(self, base_url="https://api.openweathermap.org/data/2.5/weather"):
        self.base_url = base_url
        if not OpenWeatherClient.api_key:
            raise ApiKeyNotFound(
                "API key not found. Please set API_KEY in environment variables."
            )

    def fetch_from_api(self, city):
        url = f"{self.base_url}?q={city}&appid={OpenWeatherClient.api_key}"
        try:
            response = requests.get(url, timeout=10)

            if response.status_code == 401:
                raise ApiKeyInvalid(
                    "Invalid API key. Please check your OpenWeather API key."
                )

            if response.status_code == 404:
                logger.warning(f"City '{city}' not found in OpenWeather API")
                return None

            response.raise_for_status()
            logger.info(f"Successfully fetched weather data for {city}")

            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed for city {city}: {e}")
            raise
