import datetime
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


class TransactionsSchema(BaseSchema):
    """Creates a validation schema for transactions."""

    item = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Item name is required.'}
        })
    transaction_type = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Transaction Type is required.'}
        })
    transaction_id = fields.Integer(
        required=True,
        error_messages={
            'required': {'message': 'Transaction ID is required.'}
        })
    status = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            'required': {'message': 'Status is required.'}
        })

    transaction_date = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Transaction Date is required.'}
        })

    due_date = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Due Date is required.'}
        })

    customer_or_supplier = fields.String(
        required=True,
        validate=validate.Length(min=1),
        error_messages={
            'required': {'message': 'Customer or Supplier name is required.'}
        })

    quantity = fields.Integer(
        required=True,
        error_messages={
            'required': {'message': 'Quantity is required.'}
        })

    unit_amount = fields.Float(
        required=True,
        error_messages={
            'required': {'message': 'Unit Amount is required.'}
        })

    transaction_amount = fields.Float(
        required=True,
        error_messages={
            'required': {'message': 'Transaction Amount is required.'}
        })

    @post_load
    def verify_date(self, data, **kwargs):
        """Extra validation for the Register User Schema."""
        dates = [data['due_date'], data['transaction_date']]

        for data in dates:
            try:
                datetime.datetime.strptime(data, '%d-%m-%Y')
            except:
                raise ValidationError(
                    {'message': "Incorrect data format, should be DD-MM-YYYY"})


transactions_schema = TransactionsSchema()
business_schema = BusinessSchema()
