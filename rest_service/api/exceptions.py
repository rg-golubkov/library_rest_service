"""Module with common exceptions and exceptions-handlers for rest-service
"""
from typing import Optional

from flask import jsonify

from . import bp


class APIException(Exception):
    """Base class of Exception

    Attributes:
        message: exception message
        status_code: http status code
    """
    message: Optional[str] = None
    status_code: Optional[int] = None

    def __init__(self, message: str = None, status_code: int = None):
        super().__init__()

        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return {
            'error': self.message
        }


class InvalidUsage(APIException):
    """Invalid usage api for creation object (POST-method)
    """
    status_code = 400


@bp.errorhandler(APIException)
def handle_api_exception(error: APIException):
    """APIException handling
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.errorhandler(404)
def handle_not_found(error):
    """Handling 404-error
    """
    return (jsonify({'error': 'Not Found'}), 404)
