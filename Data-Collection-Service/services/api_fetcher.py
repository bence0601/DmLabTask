import os
import logging
from datetime import datetime, timedelta

import requests

from services.db_importer import CityDataManager

logger = logging.getLogger(__name__)  

class DataCollector:
    def __init__(self):
        self.weather_data = []  




    def fetch_data_for_today(self, city):
        apikey = os.getenv("API_KEY") ## Ez csak lokál marad itt, deploy után átrakom aws secretbe,
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}" ## ez mehetne egy base url-rel a konstruktorba, és ha bővítésre kerülne az osztály, akkor függvényenként lehetne megszabni, hogy milyen plusz paraméterek kellenének az url-be

        if not apikey: ## Ide jöhet majd saját exception, 
            logging.error("API Key invalid or missing. Please make sure you have a correct one!")
            raise KeyError("API Key invalid. Please make sure you have a correct one!")
        ##Ezt ki lehetne rakni egy külön függvénybe, ami csak az api hivasert felelős
        try:
            response = requests.get(url)
            response.raise_for_status()  
            
            if response.status_code == 401:
                logging.error("API error 401: Unauthorized. Invalid API key.")
                raise Exception(f"API hiba: 401 - Unauthorized, invalid API key")
            elif response.status_code == 404:
                logging.error(f"API error 404: City '{city}' not found.")
                raise Exception(f"API hiba: 404 - City not found")
            
            data = response.json()
            self.weather_data.append(data)  

            CityDataManager.add_city_to_db(data)

            logging.info(f"Weather data for {city} for today fetched successfully.")
            return data
        
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error: {errh} - Could not fetch data for {city} for today")
            raise Exception(f"API hiba: {response.status_code}") from errh
        except requests.exceptions.RequestException as err:
            logging.error(f"Request Exception: {err} - Could not fetch data for {city} for today")
            raise Exception(f"API hiba: {response.status_code}") from err


