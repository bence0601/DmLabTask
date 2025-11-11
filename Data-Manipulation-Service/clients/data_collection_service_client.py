import requests
import logging

logger = logging.getLogger(__name__)


class DataCollectorServiceClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url

    def fetch_weather(self, city):
        response = requests.get(f"{self.base_url}/dcs/fetch-weather/{city}")
        response.raise_for_status()
        return response.json()
