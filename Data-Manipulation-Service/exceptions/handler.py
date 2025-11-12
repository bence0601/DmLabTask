from flask import jsonify
import logging

from exceptions.custom_exception import (
    DataManipulationServiceException,
    NotEnoughDataException,
)

logger = logging.getLogger(__name__)


def register_error_handler(app):
    @app.errorhandler(NotEnoughDataException)
    def handle_not_enough_data(error):
        logger.error(f"Data was insufficent for creating forecast")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Not enough weather data for creating forecast",
                    "error_code": error.error_code,
                }
            ),
            422,
        )

    @app.errorhandler(DataManipulationServiceException)
    def handle_data_manipulation_exception(error):
        logger.error(f"Data manipulation error: {error}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": error.message,
                    "error_code": error.error_code,
                }
            ),
            500,
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        logger.error(f"ValueError: {error}")
        return (
            jsonify({"status": "error", "message": f"City not found: {str(error)}"}),
            404,
        )

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        logger.error(f"Unexpected error: {error}", exc_info=True)
        return jsonify({"status": "error", "message": "Couldn't fetch data."})
