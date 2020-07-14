"""Contain utility functions and constants."""

from flask import jsonify


def response_builder(data, status_code=200):
    """Build the jsonified response to return."""
    response = jsonify(data)
    response.status_code = status_code
    return response


def validate_file(data, fields):
    """ Check for random headers"""
    if data.iloc[0, 0] != "Do not change the headers" or data.iloc[10, 1] != "Required" \
            or data.iloc[21, 0] != "Order Payment" or data.iloc[25, 2] != "Status":
        return response_builder(dict(message="The file headers are corrupted, \
            kindly upload file with correct headers"), 400)
    if data.iloc[25, 0] != "Transaction" or data.iloc[25, 1] != "ID" or data.iloc[25, 2] != "Status"\
            or data.iloc[25, 3] != "Transaction Date" or data.iloc[25, 4] != "Due Date" or data.iloc[25, 5] != \
            "Customer or Supplier" or data.iloc[25, 6] != "Item" or data.iloc[25, 7] != "Quantity":
        return response_builder(dict(message="The file headers are corrupted, \
            kindly upload file with correct headers"), 400)
    if fields.isnull().values.any():
        return response_builder(dict(message="Some of the required fields \
                are missing"), 400)
    pass
