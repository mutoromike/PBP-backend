"""Contain utility functions and constants."""

from flask import jsonify


def response_builder(data, status_code=200):
    """Build the jsonified response to return."""
    response = jsonify(data)
    response.status_code = status_code
    return response
