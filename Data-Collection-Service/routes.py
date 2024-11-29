import os
from dotenv import load_dotenv
from flask import Blueprint,jsonify,request
import requests

data_collection_bp = Blueprint("data_collection", __name__)

@data_collection_bp.route("/fetch-weather", methods=["GET"])
def fetch_weather_for_specific_day():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error: Kérlek adj meg egy városnevet!"}), 400
    
    result = fetch_data_today(city)
    
    return jsonify(result)


@data_collection_bp.route("/fetch-weather-for-days", methods=["GET"])
def fetch_weather_for_7_days():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error: Kérlek adj meg egy városnevet!"}), 400
    
    result = fetch_data_for_week(city)
    
    return jsonify(result)
    


if __name__ == '__main__':
    app.run(debug=True)
