from flask import Blueprint, jsonify, request
import requests
from services import forecast_service

data_manipulation_bp = Blueprint("data_manipulation", __name__)


@data_manipulation_bp.route("/forecast-for-city", methods=["GET"])
def create_forecast_for_city():
    pass
    # city = request.args.get("city")

    # if not city:
    #     return jsonify({"error": "Kérlek adj meg egy városnevet!"}), 400
    # forecaster = Forecast()
    # result = forecaster.create_forecast_for_city(city)
    # return jsonify(result)


# @data_manipulation_bp.route("/weather-today-for-city", methods=["GET"])
# def get_weather_for_city_today():
#     city = request.args.get('q')

#     if not city:
#         return jsonify({"error": "Kérlek adj meg egy városnevet!"}), 400
#     forecaster = Forecast()
#     result = forecaster.get_city_data_from_db(city)
#     return jsonify(result)
