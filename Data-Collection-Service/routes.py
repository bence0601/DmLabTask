from flask import Blueprint, jsonify, request
import logging
from services.api_fetcher import DataCollector
from exception import ApiKeyInvalid

logger = logging.getLogger(__name__)

data_collection_bp = Blueprint("data_collection_bp", __name__)

@data_collection_bp.route("/fetch-weather/<city>", methods=["GET"])
def fetch_weather_for_today(city):
    collector = DataCollector()
    try:
        weather_data = collector.fetch_data_for_today(city)
        return jsonify({"status": "success", "data": weather_data})
    
    except ValueError as e:  
        logger.error(f"City not found: {e}")
        return jsonify({
            "status": "error", 
            "message": f"Város nem található: {city}"
        }), 404
    
    except ApiKeyInvalid as e:
        return jsonify({
            "status": "error",
            "message": "API kulcs érvénytelen"
        }), 401
    
    except Exception as e:
        logger.error(f"Hiba történt: {e}")
        return jsonify({
            "status": "error", 
            "message": "Nem sikerült lekérni az adatokat."
        }), 500
