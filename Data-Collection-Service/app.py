import os
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

load_dotenv()

def _setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    root = logging.getLogger()
    root.setLevel(log_level)

    fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")

    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(fmt)
    root.addHandler(console)

    log_file = os.getenv("LOG_FILE")  
    if log_file:
        try:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(fmt)
            root.addHandler(file_handler)
        except Exception as e:
            logging.getLogger(__name__).warning(
                "Nem sikerült fájlba logolni (%s). Marad csak STDOUT.", e
            )

def parse_cors_origins():
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5001")
    return [o.strip() for o in raw.split(",") if o.strip()]

_setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=parse_cors_origins())

from routes import data_collection_bp  
app.register_blueprint(data_collection_bp, url_prefix="/api")

@app.route("/")
def home():
    return "Welcome to the Weather API Service!"

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("DEBUG", "true").lower() in ("1", "true", "yes")

    logger.info("Starting Flask dev server on %s:%s (debug=%s)", host, port, debug)
    app.run(host=host, port=port, debug=debug)
