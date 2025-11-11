import os
import logging
import datetime
from repositories.forecast_repository import add_forecast,get_forecast_for_city_and_date,Session
from models.forecast import ForecastModel,engine
from mappers.forecast_mapper import model_to_dto
logger = logging.getLogger(__name__)


class ForecastService:


   def check_existing_forecast(city: str) -> ForecastModel:
      today = datetime.date.today
      with Session(engine) as session:
         existing_forecast = get_forecast_for_city_and_date(session,city,today)
         if(existing_forecast is not None):
            return existing_forecast
         else:
            return None

   def create_forecast_for_city(city : str)-> ForecastModel:
      pass
     
            
            
      
                  

   




       
    

    