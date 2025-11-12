import os
import logging

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from exceptions.handler import register_error_handler


load_dotenv()

from routes import data_manipulation_bp
from models.forecast import init_db

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000", "http://data-collection-service:5001"])

register_error_handler(app)
app.register_blueprint(data_manipulation_bp, url_prefix="/dms")


@app.route("/")
def home():
    return "This is the API of Data Manipulation Service"


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    debug = True

    init_db()

    logger.info("Starting Flask dev server on %s:%s (debug=%s)", host, port, debug)
    app.run(host=host, port=port, debug=debug, use_reloader=False)
