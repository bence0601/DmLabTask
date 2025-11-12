from flask import Blueprint, jsonify, request
from services.forecast_service import ForecastService
import logging
import requests
from clients.data_collection_service_client import DataCollectorServiceClient
from mappers.forecast_mapper import model_to_dto

logger = logging.getLogger(__name__)

data_manipulation_bp = Blueprint("data_manipulation", __name__)


@data_manipulation_bp.route("/get-forecast/<city>", methods=["GET"])
def create_forecast_for_city(city):
    forecast_for_city = ForecastService.check_existing_forecast(city)
    if forecast_for_city is None:
        client = DataCollectorServiceClient()
        weather_data = client.fetch_weather(city)
        new_forecast = ForecastService.create_forecast_for_city(weather_data)
        return jsonify(new_forecast.model_dump())
    else:
        return jsonify(forecast_for_city.model_dump())
