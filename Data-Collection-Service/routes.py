from flask import Blueprint, jsonify, request
import logging
from services.api_fetcher import DataCollector

logger = logging.getLogger(__name__)

data_collection_bp = Blueprint("data_collection_bp", __name__)

# @data_collection_bp.route("/fetch-weather/<city>", methods=["GET"])
# def fetch_weather_for_today(city):
#     collector = DataCollector()
#     weather_data = collector.fetch_data_for_today(city)
#     return jsonify({"status": "success"})


@data_collection_bp.route("/fetch-weather/<city>", methods=["GET"])
def fetch_weather_for_today(city):
    collector = DataCollector()
    print(f"Calling with city: {city}")  # Debug line
    print(
        f"Method signature: {collector.fetch_data_for_today.__code__.co_varnames}"
    )  # Debug line
    weather_data = collector.fetch_data_for_today(city)
    return jsonify({"status": "success"})
