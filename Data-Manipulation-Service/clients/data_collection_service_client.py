import requests
import logging
from exceptions.custom_exception import NotEnoughDataException

logger = logging.getLogger(__name__)


class DataCollectorServiceClient:
    def __init__(self, base_url="http://data-collection-service:5001"):
        self.base_url = base_url

    def fetch_weather(self, city):
        try:
            response = requests.get(f"{self.base_url}/dcs/get-data-for-forecast/{city}")

            if response.status_code == 422:
                raise NotEnoughDataException(
                    "Not enough data for the given city, please choose another one"
                )
            if response.status_code == 404:
                logger.warning(f"City '{city}' was not found in database or api")
                return None

            response.raise_for_status()
            data = response.json()
            return data

        except requests.RequestException as e:
            logger.error(f"Request failed for city {city}:{e}")
            raise
