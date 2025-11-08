import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

from routes import data_collection_bp
from models.data_models import _init_db,engine
from services.preseeder import preseed_database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, origins="http://localhost:5001")

app.register_blueprint(data_collection_bp, url_prefix="/api")

@app.route("/")
def home():
    return "Welcome to the Weather API Service!"

if __name__ == "__main__":
    host = "0.0.0.0"   # If this wouldn't be for job interview, i would get these from .env files, but i rather not now
    port = 5000        
    debug = True     
    
    _init_db()
    preseed_database(engine)


    logger.info("Starting Flask dev server on %s:%s (debug=%s)", host, port, debug)
    app.run(host=host, port=port, debug=debug)