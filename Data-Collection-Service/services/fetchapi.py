import requests
from dotenv import load_dotenv
import os
from services.loadintodb import CityDataManager
from datetime import datetime, timedelta
import logging

load_dotenv() 

logging.basicConfig(
    level=logging.ERROR,
    filename="data_collector_errors.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class DataCollector:
    def __init__(self):
        self.weather_data = []  

    def fetch_data_for_today(self, city):
        apikey = os.getenv("API_KEY")
        url = os.getenv("BASE_URL")
        if not apikey:
            logging.error("API Key invalid. Please make sure you have a correct one!")
            raise ValueError("API Key invalid. Please make sure you have a correct one!")
        date_format = "%Y-%m-%d"   
        today = datetime.today().strftime(date_format)

        full_url = f"{url}?key={apikey}&q={city}&aqi=no&dt={today}"
        try:
            response = requests.get(full_url)
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

            logging.info(f"Weather data for {city} on {today} fetched successfully.")
            return data
        
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error: {errh} - Could not fetch data for {city} on {today}")
            raise Exception(f"API hiba: {response.status_code}") from errh
        except requests.exceptions.RequestException as err:
            logging.error(f"Request Exception: {err} - Could not fetch data for {city} on {today}")
            raise Exception(f"API hiba: {response.status_code}") from err

    def fetch_data_for_week(self, city):
        apikey = os.getenv("API_KEY")
        url = os.getenv("BASE_URL")

        today = datetime.today()
        date_format = "%Y-%m-%d"
        date_list = [(today - timedelta(days=i)).strftime(date_format) for i in range(7)]
        
        all_data = []  

        for day in date_list:
            full_url = f"{url}?key={apikey}&q={city}&aqi=no&dt={day}"
            try:
                response = requests.get(full_url)
                response.raise_for_status()  
                
                if response.status_code == 401:
                    logging.error("API error 401: Unauthorized. Invalid API key.")
                    raise Exception(f"API hiba: 401 - Unauthorized, invalid API key")
                elif response.status_code == 404:
                    logging.error(f"API error 404: City '{city}' not found.")
                    raise Exception(f"API hiba: 404 - City not found")
                
                data = response.json()
                self.weather_data.append(data)  
                all_data.append(data)  

                CityDataManager.add_city_to_db(data)

                logging.info(f"Weather data for {city} on {day} fetched successfully.")
            
            except requests.exceptions.HTTPError as errh:
                logging.error(f"HTTP Error: {errh} - Could not fetch data for {city} on {day}")
                raise Exception(f"API hiba: {response.status_code}") from errh
            except requests.exceptions.RequestException as err:
                logging.error(f"Request Exception: {err} - Could not fetch data for {city} on {day}")
                raise Exception(f"API hiba: {response.status_code}") from err
            
        return all_data  
