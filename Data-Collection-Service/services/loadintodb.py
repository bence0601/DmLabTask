import os
import pyodbc
from dotenv import load_dotenv
from datetime import datetime



class CityDataManager():
    @staticmethod   
    def GetCityIdFromDb(city):
        load_dotenv()
        db_connection_string = os.getenv("DB_CONNECTION_STRING")

        try:

            connection = pyodbc.connect(db_connection_string)
            cursor = connection.cursor()
            
            query = """SELECT id FROM cities WHERE city_name = ?;"""
            cursor.execute(query, (str(city),))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Hiba történt a város ellenőrzése közben: {e}")
            return None
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
                
    @staticmethod
    def CheckIfCityExistsOnDate(city_id,date):
        load_dotenv()
        db_connection_string = os.getenv("DB_CONNECTION_STRING")

        try:
            connection = pyodbc.connect(db_connection_string)
            cursor = connection.cursor()
            
            query = """SELECT 1 FROM aggregatedweatherdata WHERE city_id = ? AND date = ?;"""
            cursor.execute(query, (city_id, date))
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Hiba történt a város és dátum ellenőrzése közben: {e}")
            return False
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()
        
        
    @staticmethod           
    def addCityToDb(data):
        load_dotenv()
        db_connection_string = os.getenv("DB_CONNECTION_STRING")
        try:
            connection = pyodbc.connect(db_connection_string)
            cursor = connection.cursor()
            
            city_name = data["location"]["name"]
            city_id = CityDataManager.GetCityIdFromDb(city_name)
            
            # Check if the city exists
            if city_id:
                date = data["forecast"]["forecastday"][0]["date"]
                # Check if there is already data for the given date
                if CityDataManager.CheckIfCityExistsOnDate(city_id, date):
                    print(f"Adatok már léteznek a városra ({city_name}) és a dátumra ({date}).")
                    pass  # No action needed if data exists
                else:
                    print(f"Adatok nem léteznek a városra ({city_name}) és a dátumra ({date}). Felvesszük őket.")
                    
                    # Insert hourly weather data
                    hourly_data = data["forecast"]["forecastday"][0]["hour"]
                    for record in hourly_data:
                        query = """
                            INSERT INTO weatherdata (city_id, date, hour, temp_c, wind_mph, precip_mm)
                            VALUES (?, ?, ?, ?, ?, ?);
                        """
                        cursor.execute(
                            query,
                            (
                                city_id,
                                datetime.strptime(record["time"], "%Y-%m-%d %H:%M").date(),
                                datetime.strptime(record["time"], "%Y-%m-%d %H:%M").hour,
                                record["temp_c"],
                                record["wind_mph"],
                                record["precip_mm"]
                            )
                        )

                    # Insert aggregated weather data
                    aggregated_data = data["forecast"]["forecastday"][0]["day"]
                    query = """
                        INSERT INTO aggregatedweatherdata
                        (city_id, date, max_temp_c, min_temp_c, avg_temp_c, 
                        min_wind_mph, max_wind_mph, avg_wind_mph, 
                        min_precip_mm, max_precip_mm, avg_precip_mm)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """
                    cursor.execute(
                        query,
                        (
                            city_id,
                            datetime.strptime(date, "%Y-%m-%d").date(),
                            aggregated_data["maxtemp_c"],
                            aggregated_data["mintemp_c"],
                            aggregated_data["avgtemp_c"],
                            0,  # Default for min_wind_mph (not provided in API)
                            aggregated_data["maxwind_mph"],
                            aggregated_data["maxwind_mph"],  # Placeholder for avg wind mph
                            0,  # Default for min_precip_mm
                            aggregated_data["totalprecip_mm"],
                            aggregated_data["totalprecip_mm"],  # Placeholder for avg precip
                        )
                    )

                    # Commit all changes
                    connection.commit()

            else:
                # If the city doesn't exist, first insert the city into the cities table
                print(f"A város ({city_name}) még nem létezik, tehát először felvesszük a cities táblába.")
                
                # Insert the city into the cities table
                query = "INSERT INTO cities (city_name) VALUES (?);"
                cursor.execute(query, (city_name,))
                connection.commit()

                # Get the city ID
                cursor.execute("SELECT id FROM cities WHERE city_name = ?;", (city_name,))
                city_id = cursor.fetchone()[0]

                # Insert hourly weather data
                hourly_data = data["forecast"]["forecastday"][0]["hour"]
                for record in hourly_data:
                    query = """
                        INSERT INTO weatherdata (city_id, date, hour, temp_c, wind_mph, precip_mm)
                        VALUES (?, ?, ?, ?, ?, ?);
                    """
                    cursor.execute(
                        query,
                        (
                            city_id,
                            datetime.strptime(record["time"], "%Y-%m-%d %H:%M").date(),
                            datetime.strptime(record["time"], "%Y-%m-%d %H:%M").hour,
                            record["temp_c"],
                            record["wind_mph"],
                            record["precip_mm"]
                        )
                    )

                # Insert aggregated weather data
                aggregated_data = data["forecast"]["forecastday"][0]["day"]
                query = """
                    INSERT INTO aggregatedweatherdata
                    (city_id, date, max_temp_c, min_temp_c, avg_temp_c, 
                    min_wind_mph, max_wind_mph, avg_wind_mph, 
                    min_precip_mm, max_precip_mm, avg_precip_mm)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """
                cursor.execute(
                    query,
                    (
                        city_id,
                        datetime.strptime(data["forecast"]["forecastday"][0]["date"], "%Y-%m-%d").date(),
                        aggregated_data["maxtemp_c"],
                        aggregated_data["mintemp_c"],
                        aggregated_data["avgtemp_c"],
                        0,  # Default for min_wind_mph (not provided in API)
                        aggregated_data["maxwind_mph"],
                        aggregated_data["maxwind_mph"],  # Placeholder for avg wind mph
                        0,  # Default for min_precip_mm
                        aggregated_data["totalprecip_mm"],
                        aggregated_data["totalprecip_mm"],  # Placeholder for avg precip
                    )
                )

                # Commit all changes
                connection.commit()

        except Exception as e:
            print(f"Error while adding city data to the database: {e}")
            if connection:
                connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            

            
        
            
            
        