import logging

logger = logging.getLogger(__name__)


class DataManipulationServiceException(Exception):
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"{self.message} (Error Code: {self.error_code})"
        return self.message


class NotEnoughDataException(DataManipulationServiceException):
    """Raised when there's not enough data to create a forecast"""

    pass
