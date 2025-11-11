from flask import jsonify
import logging

from exceptions.custom_exception import (
    ApiKeyInvalid,
    ApiKeyNotFound,
    DataCollectionServiceException,
)

logger = logging.getLogger(__name__)

def register_error_handler(app):
    @app.errorhandler(ApiKeyNotFound)
    def handle_api_key_not_found(error):
        logger.error(f"API key not found: {error}")
        return jsonify({
            "status": "error",
            "message": "API key not found in configuration file",
            "error_code": error.error_code,
        }), 500

    @app.errorhandler(ApiKeyInvalid)
    def handle_api_key_invalid(error):
        logger.error(f"API key invalid: {error}")
        return jsonify({
            "status": "error",
            "message": "API key invalid",
            "error_code": error.error_code,
        }), 401

    @app.errorhandler(DataCollectionServiceException)
    def handle_data_collection_exception(error):
        logger.error(f"Data collection error: {error}")
        return jsonify({
            "status": "error",
            "message": error.message,
            "error_code": error.error_code,
        }), 500

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        logger.error(f"ValueError: {error}")
        return jsonify({
            "status": "error",
            "message": f"City not found: {str(error)}"
        }), 404

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        logger.error(f"Unexpected error: {error}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Couldn't fetch data."})
