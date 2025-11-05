from flask import Blueprint, jsonify, request
import logging
from services.fetchapi import DataCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

data_collection_bp = Blueprint("data_collection", __name__)

@data_collection_bp.route("/fetch-weather", methods=["GET"])
def fetch_weather_for_today():
    city = request.args.get('city')
    if not city:
        return jsonify({"status": "error", "message": "Kérlek adj meg egy városnevet!"}), 400

    collector = DataCollector()
    try:
        weather_data = collector.fetch_data_for_today(city)
        return jsonify({"status": "success", "data": weather_data})
    except Exception as e:
        logger.error(f"Hiba történt az időjárás lekérése során: {e}")
        return jsonify({"status": "error", "message": "Nem sikerült lekérni az adatokat."}), 500


