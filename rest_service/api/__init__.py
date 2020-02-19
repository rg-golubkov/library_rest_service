"""REST-API for library service

URLS:
    /books/<Optional: book_id>
    /authors/<Optional: author_id>
"""
from flask import Blueprint


bp = Blueprint('api', __name__, url_prefix='/api')

from .authors import AuthorAPI
from .books import BookAPI
from .base import register_api

register_api(AuthorAPI, 'authors_api', '/authors/', pk='pk')
register_api(BookAPI, 'books_api', '/books/', pk='pk')
