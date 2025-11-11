from flask import Blueprint, jsonify, request
import requests
from services.forecast_service import ForecastService
import logging
import requests

logger = logging.getLogger(__name__)

data_manipulation_bp = Blueprint("data_manipulation", __name__)

def _fetch_weather_from_collection_service(city):
    base_url = "http://localhost:5001" 
    response = requests.get(f"{base_url}/fetch-weather/{city}")

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f'Error:{response.status_code}')
        return None

@data_manipulation_bp.route("/get-forecast/<city>", methods=["GET"])
def create_forecast_for_city(city):
    forcast_service = ForecastService()
    forecast_for_city = forcast_service.check_existing_forecast(city)
    if forecast_for_city is None:
        _fetch_weather_from_collection_service(city)
    else:
        new_forecast = forcast_service.create_forecast_for_city(city)
        return jsonify(new_forecast)
        