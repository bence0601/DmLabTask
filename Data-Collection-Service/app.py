import os
import logging

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

from routes import data_collection_bp
from models.data_models import init_db, engine
from database.preseeder import preseed_database
from exceptions.handler import register_error_handler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, origins="http://data-manipulation-service:5000")

register_error_handler(app)
app.register_blueprint(data_collection_bp, url_prefix="/dcs")


@app.route("/")
def home():
    return "Welcome to the Weather API Service!"


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5001
    debug = True

    init_db()
    preseed_database(engine)

    logger.info("Starting Flask dev server on %s:%s (debug=%s)", host, port, debug)
    app.run(host=host, port=port, debug=debug, use_reloader=False)
