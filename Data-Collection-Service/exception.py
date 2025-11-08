import logging

logger = logging.getLogger(__name__)


class DataCollectionServiceException(Exception):
    """Base Exception"""

    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"{self.message} (Error Code: {self.error_code})"
        return self.message


class ApiKeyNotFound(DataCollectionServiceException):
    """Raised when an Api Key is not found in .env file"""

    pass


class ApiKeyInvalid(DataCollectionServiceException):
    """Raised when Open Weather Api throws unauthorized, for missing api key"""

    pass


## If i would add retry-mechanism or other exception handling,
# it would be nice to create a handle_exception() functions,
# so there would be less boilerplate code through the codebase
