"""REST-API for interact with books data
"""
from flask import request

from ..models import Author, Book
from .auth import token_required
from .base import BaseAPI
from .exceptions import InvalidUsage


class BookAPI(BaseAPI):
    model = Book
    namespace = 'books'
    decorators = [token_required]

    def create_record(self):
        self._validate_request_data(request.json)

        if 'title' not in request.json:
            raise InvalidUsage('Titile is required')
        if 'pub_year' not in request.json:
            raise InvalidUsage('Publication year is required')

        return Book.fromdict(request.json)

    def update_record(self, record):
        self._validate_request_data(request.json)

        if 'title' in request.json:
            record.title = request.json.get('title')

        if 'pub_year' in request.json:
            record.publication_year = request.json.get('pub_year')

        if 'author_id' in request.json:
            record.author_id = request.json.get('author_id')

        return record

    def _validate_request_data(self, request_json: dict) -> bool:
        if not request_json:
            raise InvalidUsage('Sent data is empty')

        if 'title' in request_json:
            title = request_json.get('title')
            if not title or not isinstance(title, str):
                raise InvalidUsage('Title must be a non-empty string')

        if 'pub_year' in request_json:
            pub_year = request_json.get('pub_year')
            if pub_year is None or not isinstance(pub_year, int):
                raise InvalidUsage('Publication year must be an integer')

        author_id = request_json.get('author_id')
        if author_id:
            if isinstance(author_id, int):
                author = Author.query.get(author_id)
                if author is None:
                    raise InvalidUsage(
                        f'Author with {author_id} id is not exist'
                    )
            else:
                raise InvalidUsage('Author ID must be an integer')

        return True
