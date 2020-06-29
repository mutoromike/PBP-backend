from datetime import date
from marshmallow import (Schema, ValidationError, fields, post_load, validate,
                         validates_schema)

from api.utils.marshmallow_schemas import BaseSchema

from .models import Business


class BusinessSchema(BaseSchema):
    """Creates a validation schema for business featiures."""

    name = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Business name is required.'}
        })
    abbreviated_name = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Name Abbreviation is required.'}
        })
    address = fields.String(
        required=True,
        error_messages={
            'required': {'message': 'Business Address is required.'}
        })
    country = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            'required': {'message': 'Country is required.'}
        })

    entity = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Entity is required.'}
        })
    
    revenue = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Revenue is required.'}
        })

    accounting_software = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Accounting software is required.'}
        })

    countries = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Countries is/are required.'}
        })

business_schema = BusinessSchema()
