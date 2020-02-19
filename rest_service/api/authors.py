"""REST-API for interact with authors data
"""
from flask import request

from ..models import Author
from .auth import token_required
from .base import BaseAPI
from .exceptions import InvalidUsage


class AuthorAPI(BaseAPI):
    model = Author
    namespace = 'authors'
    decorators = [token_required]

    def create_record(self):
        self._validate_request_data(request.json)

        if 'fullname' not in request.json:
            raise InvalidUsage('Full name is required')

        return Author.fromdict(request.json)

    def update_record(self, record):
        self._validate_request_data(request.json)

        if 'fullname' in request.json:
            record.fullname = request.json.get('fullname')

        return record

    def _validate_request_data(self, request_json: dict) -> bool:
        if not request_json:
            raise InvalidUsage('Sent data is empty')

        if 'fullname' in request_json:
            fullname = request_json.get('fullname')
            if not fullname or not isinstance(fullname, str):
                raise InvalidUsage('Full name must be a non-empty string')

        return True
