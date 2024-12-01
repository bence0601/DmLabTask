from flask import Blueprint,jsonify,request
import requests

data_manipulation_bp = Blueprint("data_manipulation", __name__)


@data_manipulation_bp.route("/forecast-for-city", methods=["GET"])
def create_forecast_for_city():
    pass



   