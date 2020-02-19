"""Module for authentication and authorization methods
"""
from flask import abort


def token_required(func):
    def inner(*args, **kwargs):
        if not verify_token():
            abort(401)
        return func(*args, **kwargs)
    return inner


def verify_token(*args, **kwargs) -> bool:
    """Check token from request
    """
    # TODO: Add implementation
    return True
