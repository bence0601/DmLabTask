import requests
from dotenv import load_dotenv
import os
from services.loadintodb import CityDataManager
from datetime import datetime, timedelta

load_dotenv() 

class DataCollector:
    def __init__(self):
        self.weather_data = []  
        
    def fetch_data_for_today(self,city):
        apikey = os.getenv("API_KEY")
        url = os.getenv("BASE_URL")
        if not apikey:
            raise ValueError("API Key invalid. Please make sure you have a correct one!")
        date_format = "%Y-%m-%d"   
        today = datetime.today().strftime(date_format)


        full_url = f"{url}?key={apikey}&q={city}&aqi=no&dt={today}"
        try:
                response = requests.get(full_url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                
                if response.status_code == 401:
                    raise Exception(f"API hiba: 401 - Unauthorized, invalid API key")
                elif response.status_code == 404:
                    raise Exception(f"API hiba: 404 - City not found")
                
                data = response.json()
                self.weather_data.append(data)  

                CityDataManager.addCityToDb(data)

                print(f"Weather data for {city} on {today} fetched successfully.")
                return data
            
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh} - Could not fetch data for {city} on {today}")
            # We re-raise the exception with the correct format for tests
            raise Exception(f"API hiba: {response.status_code}") from errh
        except requests.exceptions.RequestException as err:
            print(f"Error: {err} - Could not fetch data for {city} on {today}")
            # Handle any other errors (like connectivity issues)
            raise Exception(f"API hiba: {response.status_code}") from err

    def fetch_data_for_week(self,city):
        apikey = os.getenv("API_KEY")
        url = os.getenv("BASE_URL")

        today = datetime.today()
        date_format = "%Y-%m-%d"
        date_list = [(today - timedelta(days=i)).strftime(date_format) for i in range(7)]
        
        all_data = []  # Lista az összes nap adatainak tárolására

        
        for day in date_list:
            full_url = f"{url}?key={apikey}&q={city}&aqi=no&dt={day}"
            try:
                response = requests.get(full_url)
                response.raise_for_status()  # Raise HTTPError for bad responses
                
                if response.status_code == 401:
                    raise Exception(f"API hiba: 401 - Unauthorized, invalid API key")
                elif response.status_code == 404:
                    raise Exception(f"API hiba: 404 - City not found")
                
                data = response.json()
                self.weather_data.append(data)  
                all_data.append(data)  # Az aktuális nap adatait hozzáadjuk az összeshez


                CityDataManager.addCityToDb(data)

                print(f"Weather data for {city} on {day} fetched successfully.")
            
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error: {errh} - Could not fetch data for {city} on {day}")
                # We re-raise the exception with the correct format for tests
                raise Exception(f"API hiba: {response.status_code}") from errh
            except requests.exceptions.RequestException as err:
                print(f"Error: {err} - Could not fetch data for {city} on {day}")
                # Handle any other errors (like connectivity issues)
                raise Exception(f"API hiba: {response.status_code}") from err
            
        return all_data  # Az összes nap adatainak visszaadása
