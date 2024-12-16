import os
import pyodbc
from datetime import datetime, timedelta
import requests
from sqlalchemy import create_engine, Column, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from dotenv import load_dotenv
import logging

load_dotenv()

# Logger beállítása
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Forecast:

    @staticmethod
    def _get_connection():
        db_connection_string = os.getenv("DB_CONNECTION_STRING_FOR_QUERIES")
        if not db_connection_string:
            logger.error("DB_CONNECTION_STRING_FOR_QUERIES environment variable is not set.")
            raise ValueError("Database connection string is missing.")
        
        try:
            return pyodbc.connect(db_connection_string)
        except pyodbc.Error as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise

    @staticmethod
    def check_for_fresh_weather_data(city_id):
        date_format = "%Y-%m-%d"
        today = datetime.today().strftime(date_format)
        six_days_ago = (datetime.today() - timedelta(days=6)).strftime(date_format)

        query = """
            SELECT COUNT(*) 
            FROM aggregatedweatherdata 
            WHERE city_id = ? 
            AND date BETWEEN ? AND ?;
        """
        
        try:
            with Forecast._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (city_id, six_days_ago, today))
                    result = cursor.fetchone()
            
            return result[0] == 7
        except pyodbc.Error as e:
            logger.error(f"Database error occurred while checking weather data: {e}")
            return False

    @staticmethod
    def get_id_of_city(city):
        query = """
        SELECT id
        FROM cities
        WHERE city_name = ?;
        """
        
        try:
            with Forecast._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (city,))
                    result = cursor.fetchone()

                    if result is None:
                        logger.warning(f"City '{city}' not found in the database.")
                        return None

                    return result[0]
        except pyodbc.Error as e:
            logger.error(f"Error retrieving city ID for '{city}': {e}")
            return None

    @staticmethod
    def fetch_weather_data_if_needed(city):
        base_url = "http://localhost:5000/fetch-weather-for-days"
        
        params = {"q": city}
        try:
            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                return response.json()  
            else:
                logger.error(f"Failed to fetch weather data. Status code: {response.status_code}")
                return {
                    "error": f"Failed to fetch weather data. Status code: {response.status_code}",
                    "details": response.text
                }
        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred while fetching weather data: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    @staticmethod
    def forecast_logic(city_id, city):
        today = datetime.today().strftime("%Y-%m-%d")
        six_days_ago = (datetime.today() - timedelta(days=6)).strftime("%Y-%m-%d")

        query = """
        SELECT date, avg_temp_c, avg_wind_mph, avg_precip_mm 
        FROM aggregatedweatherdata 
        WHERE city_id = ? 
        AND date BETWEEN ? AND ?
        ORDER BY date;
        """

        try:
            with Forecast._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (city_id, six_days_ago, today))
                    rows = cursor.fetchall()
        except pyodbc.Error as e:
            logger.error(f"Database error occurred while fetching forecast data: {e}")
            return None
        
        if len(rows) != 7:  
            logger.warning(f"Only {len(rows)} records found, expected 7.")
            return None

        dates = []
        temps = []
        winds = []  
        precips = []  

        for row in rows:
            dates.append(row[0])  
            temps.append(row[1]) 
            winds.append(row[2])  
            precips.append(row[3])  

        query_additional = """
        SELECT date, avg_temp_c, avg_wind_mph, avg_precip_mm 
        FROM aggregatedweatherdata 
        WHERE city_id = ? 
        AND date < ?  
        ORDER BY date DESC;
        """

        try:
            with Forecast._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_additional, (city_id, six_days_ago))
                    additional_rows = cursor.fetchall()
        except pyodbc.Error as e:
            logger.error(f"Database error occurred while fetching additional data: {e}")
            return None

        last_date = dates[-1]
        for row in additional_rows:
            current_date = row[0]
            if (last_date - current_date).days <= 3:
                dates.append(row[0])  
                temps.append(row[1])  
                winds.append(row[2])  
                precips.append(row[3])  
                last_date = current_date  
            else:
                break  

        if len(dates) < 7:
            logger.warning("Not enough data available for forecasting.")
            return None

        X = list(range(len(dates))) 
        X = [[x] for x in X] 
        
        y_temp = temps
        model_temp = LinearRegression().fit(X, y_temp)
        temp_forecast = model_temp.predict([[len(dates)], [len(dates) + 1], [len(dates) + 2]]) 

        y_wind = winds
        model_wind = LinearRegression().fit(X, y_wind)
        wind_forecast = model_wind.predict([[len(dates)], [len(dates) + 1], [len(dates) + 2]])

        y_precip = precips
        model_precip = LinearRegression().fit(X, y_precip)
        precip_forecast = model_precip.predict([[len(dates)], [len(dates) + 1], [len(dates) + 2]])

        forecast = {
            "city": city,
            "forecast": {
                "day_1": {
                    "temperature": temp_forecast[0],
                    "wind_speed": wind_forecast[0],
                    "precipitation": precip_forecast[0],
                },
                "day_2": {
                    "temperature": temp_forecast[1],
                    "wind_speed": wind_forecast[1],
                    "precipitation": precip_forecast[1],
                },
                "day_3": {
                    "temperature": temp_forecast[2],
                    "wind_speed": wind_forecast[2],
                    "precipitation": precip_forecast[2],
                },
            },
        }

        return forecast

    @staticmethod
    def create_forecast_for_city(city):
        existing_id = Forecast.get_id_of_city(city)
        if existing_id is None:
            logger.info(f"City '{city}' is not found in the database. Fetching new data.")
            city_data_from_api = Forecast.fetch_weather_data_if_needed(city)

            if not city_data_from_api:
                logger.error(f"Cannot forecast weather for city '{city}' as there is no data in the central DB.")
                return None
            else:
                return Forecast.forecast_logic(existing_id, city)
        else:
            data_from_last_week = Forecast.check_for_fresh_weather_data(existing_id)
            if data_from_last_week:
                return Forecast.forecast_logic(existing_id, city)
            else:
                city_data_from_api = Forecast.fetch_weather_data_if_needed(city)
                return Forecast.forecast_logic(existing_id, city)
