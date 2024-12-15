import os
import pyodbc
from dotenv import load_dotenv
from datetime import datetime
import logging


# Alapértelmezett környezeti változók betöltése egyszer
load_dotenv()


# Beállítjuk a naplózást
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CityDataManager:

    @staticmethod
    def _get_connection():
        """Database connection helper"""
        db_connection_string = os.getenv("DB_CONNECTION_STRING")
        return pyodbc.connect(db_connection_string)

    @staticmethod
    def _convert_to_datetime(date_str, format="%Y-%m-%d %H:%M"):
        """Utility to convert string to datetime object"""
        return datetime.strptime(date_str, format)

    @staticmethod
    def GetCityIdFromDb(city):
        """Get the city ID from the database based on city name"""
        try:
            with CityDataManager._get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """SELECT id FROM cities WHERE city_name = ?;"""
                    cursor.execute(query, (str(city),))
                    result = cursor.fetchone()
                    return result[0] if result else None
        except Exception as e:
            logging.error(f"Error while checking city: {e}")
            return None

    @staticmethod
    def CheckIfCityExistsOnDate(city_id, date):
        """Check if data exists for a specific city and date"""
        try:
            with CityDataManager._get_connection() as connection:
                with connection.cursor() as cursor:
                    query = """SELECT 1 FROM aggregatedweatherdata WHERE city_id = ? AND date = ?;"""
                    cursor.execute(query, (city_id, date))
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logging.error(f"Error while checking city and date: {e}")
            return False

    @staticmethod
    def addCityToDb(data):
        """Add city and weather data to the database"""
        city_name = data["location"]["name"]
        city_id = CityDataManager.GetCityIdFromDb(city_name)

        try:
            with CityDataManager._get_connection() as connection:
                with connection.cursor() as cursor:
                    # Insert city if not exists
                    if not city_id:
                        logging.info(f"City {city_name} does not exist, inserting...")
                        cursor.execute("INSERT INTO cities (city_name) VALUES (?);", (city_name,))
                        connection.commit()
                        city_id = cursor.execute("SELECT id FROM cities WHERE city_name = ?;", (city_name,)).fetchone()[0]

                    date = data["forecast"]["forecastday"][0]["date"]
                    if CityDataManager.CheckIfCityExistsOnDate(city_id, date):
                        logging.info(f"Data already exists for city {city_name} and date {date}. Skipping.")
                        return

                    logging.info(f"Adding data for city {city_name} and date {date}.")
                    
                    # Prepare and insert hourly data
                    hourly_data = data["forecast"]["forecastday"][0]["hour"]
                    records = [
                        (
                            city_id,
                            CityDataManager._convert_to_datetime(record["time"]).date(),
                            CityDataManager._convert_to_datetime(record["time"]).hour,
                            record["temp_c"],
                            record["wind_mph"],
                            record["precip_mm"]
                        )
                        for record in hourly_data
                    ]
                    cursor.executemany("""
                        INSERT INTO weatherdata (city_id, date, hour, temp_c, wind_mph, precip_mm)
                        VALUES (?, ?, ?, ?, ?, ?);
                    """, records)

                    # Prepare and insert aggregated data
                    aggregated_data = data["forecast"]["forecastday"][0]["day"]
                    cursor.execute("""
                        INSERT INTO aggregatedweatherdata
                        (city_id, date, max_temp_c, min_temp_c, avg_temp_c, 
                        min_wind_mph, max_wind_mph, avg_wind_mph, 
                        min_precip_mm, max_precip_mm, avg_precip_mm)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        city_id,
                        CityDataManager._convert_to_datetime(date, "%Y-%m-%d").date(),
                        aggregated_data["maxtemp_c"],
                        aggregated_data["mintemp_c"],
                        aggregated_data["avgtemp_c"],
                        0,  # Default for min_wind_mph
                        aggregated_data["maxwind_mph"],
                        aggregated_data["maxwind_mph"],  # Placeholder for avg wind mph
                        0,  # Default for min_precip_mm
                        aggregated_data["totalprecip_mm"],
                        aggregated_data["totalprecip_mm"],  # Placeholder for avg precip
                    ))

                    connection.commit()

        except Exception as e:
            logging.error(f"Error while adding city data to the database: {e}")
            if connection:
                connection.rollback()
